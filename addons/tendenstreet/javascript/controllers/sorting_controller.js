import { Controller } from 'stimulus'
// import StimulusReflex from 'stimulus_reflex'
import 'blissfuljs/bliss.shy.js'
import 'blissfuljs/bliss._.js'
import { keepOriginalOrder } from 'webpack/lib/util/comparators'
// import { update } from 'timm'
import voca from 'voca'


export default class extends Controller {
  static targets = [
    'template', 'display', 'nav', 'cta', 'grid', 'item',
    'categories', 'catBtn', 'filters', 'filterBtn', 'sorts', 'sortBtn'
  ]

  initialize() {
    this.element[this.identifier] = this
  }

  connect() {
    // StimulusReflex.register(this)

    console.log(this)

    try {
      this.categories = new Set(this.data.get('categories').split(' '))
    }
    catch {
      this.categories = new Set()
    }
    this.filters = new Set()

    // Take a copy of the server-rendered contents. We will be sorting and filtering from this.
    this.original = this.gridTargets.map(t => t.cloneNode(true))
    // this.gridTargets.map(t => console.log(t))

    // The controller's display is constructed in markup inside `<template>` tags, so that the server-side template renderer is empowered to determine the layout of the interface. All tags inside `template` will be cloned to a controller-generated `div` immediately following `template` under the same parent. This opens up potential expansion of the presentation behavior to allow for multiple templates, in the case of a complex interface with additional features or composed controllers.

    // Elements inside `template` aren't rendered, so the controller doesn't see them as targets.
    if (this.hasTemplateTarget) {
      let elements = Array.from(this.templateTarget.content.children).map( t => t.cloneNode(true) )
      // You need `.content` to get inside the `#document-fragment` inside the `template` tag.
      for (let i in elements)
        this.displayTarget.appendChild(elements[i])
    }


    if (this.itemTargets) {
      // If we have items, build the nav display.
      this.digest_items()
      // this.call_to_action()
      this.add_filters()
    }
  }

  digest_items() {
    for (let i in this.itemTargets) {
      let item = this.itemTargets[i]
      let metadata = JSON.parse(item.getAttribute("data-sorting-metadata"))

      if (typeof metadata === 'object' && metadata !== null) {
        let attrs = Object.entries(metadata)
        
        for (let i in attrs) {
          let attr = attrs[i]
          
          if (attr[0] == "category") {
            item.setAttribute("data-sorting-category", attr[1])
            this.categories.add(attr[1])
          }
          else if (attr[0] == "filters") {
            item.setAttribute("data-sorting-filters", attr[1].join(" "))
            
            for (let filter of attr[1])
              this.filters.add(filter)
          }
          else {
            item.setAttribute("data-sorting-" + attr[0], attr[1])
          }
        }

      }
    }
  }

  call_to_action() {
    if (this.hasCtaTarget) {
      this.templateTarget._.after(this.ctaTarget.cloneNode(true))
    }
  }

  deslugify(str) {
    return voca.titleCase(voca.replaceAll(str, '-', ' '))
  }

  add_filters() {
    // When you click on a feature filter, all feature filter buttons remain visible. When you click on a category filter, all feature filter buttons for hidden items are also hidden and all category filter buttons remain visible.
    if (!this.filters)
      return

    let extract = (target) => target.removeChild(target.firstElementChild)
    
    if (this.hasCategoriesTarget) {
      let proto = extract(this.categoriesTarget)
      let buttons = Array.from(this.categories).filter(e => e).map((cat) => {
        let copy = proto.cloneNode(true)
        let btn = copy.firstElementChild

        btn.innerText = this.deslugify(cat)
        btn.setAttribute('name', cat)

        return copy
      })

      for (let i in buttons)
        this.categoriesTarget.appendChild(buttons[i])
    }

    if (this.hasFiltersTarget) {
      let proto = extract(this.filtersTarget)
      let buttons = Array.from(this.filters).sort().filter(e => e).map((filter) => {
        let copy = proto.cloneNode(true)
        let btn = copy.firstElementChild

        btn.innerText = this.deslugify(filter)
        btn.setAttribute('name', filter)

        return copy
      })

      for (let i in buttons)
        this.filtersTarget.appendChild(buttons[i])
    }
  }

  add_sorts() {
    // Sorts should never change what appears, only where.

    if (this.filters) {
      let buttons = []
      let categories = []
      
      for (let filter in this.filters) {
        if (filter in this.options.categories)
          categories.push({
            "tag": "li",
            "className": "",
            "contents": {
              "tag": "button",
              "className": this.classNames['cat-btn'],
              "contents": voca.titleCase(filter),
              "attributes": {
                "type": "button",
                "name": filter,
                "aria-pressed": false,
                "data-action": "click->sorting#filter"
              }
            }
          })
        else
          buttons.push({
            "tag": "li",
            "className": "",
            "contents": {
              "tag": "button",
              "className": this.classNames['filter-btn'],
              "contents": voca.titleCase(filter),
              "attributes": {
                "type": "button",
                "name": filter,
                "aria-pressed": false,
                "data-action": "click->sorting#filter"
              }
            }
          })
      }

      cat_list = {}
      if (categories)
        cat_list = {
          "tag": "ul",
          "id": "sorting-cat-list",
          "className": this.classNames['cat-list'],
          "contents": categories,
          "attributes": {
            "data-target": "sorting.categories"
          }
        }

      this.navTarget._.inside([
        {
          "tag": "label",
          "className": this.classNames['sort-label'],
          "contents": "Filters:",
          "attributes": {
            "for": "sorting-sorts"
          }
        },
        {
          "tag": "ul",
          "id": "sorting-sorts",
          "className": this.classNames['sort-list'],
          "contents": buttons,
          "attributes": {
            "data-target": "sorting.sorts"
          }
        }
      ])
    }
  }

  filter(event) {
    // Toggle or untoggle the selected button and update 
    const button = event.currentTarget
    const filterFn = button.getAttribute('name')

    let activate = () => {
      var pressed = (button.getAttribute("aria-pressed") === "true")
      
      if (pressed)
        button.setAttribute('aria-pressed', 'false')
      else
        button.setAttribute('aria-pressed', 'true')

      return (!pressed)
    }

    let elems = []
    let active_cats = []
    let active_filters = []

    let activated = activate()

    console.log(filterFn)

    // If a category was activated, forcibly deactivate all other categories.
    if (activated && Array.from(this.categories).includes(filterFn)) {
      this.categoriesTarget.querySelectorAll('button').forEach(e => {
        if (e.getAttribute('name') != filterFn)
          e.setAttribute('aria-pressed', 'false')
      })
    }
    active_cats = Array.from(
      this.categoriesTarget.children
    ).filter(
      (i) => (i.firstElementChild.getAttribute("aria-pressed") === "true")
    ).map(
      (i) => i.firstElementChild.getAttribute('name')
    )

    if (active_cats.length)
      this.categoriesTarget.setAttribute('active', "")
    else
      this.categoriesTarget.removeAttribute('active')

    active_filters = Array.from(
      this.filtersTarget.children
    ).filter(
      (i) => (i.firstElementChild.getAttribute("aria-pressed") === "true")
    ).map(
      (i) => i.firstElementChild.getAttribute('name')
    )

    if (active_filters.length)
      this.filtersTarget.setAttribute('active', "")
    else
      this.filtersTarget.removeAttribute('active')

    elems = this.run_filters(this.original, active_filters)

    this.update_grid(elems)
  }

  run_filters(targets, filters) {
    let elems = []

    // TODO: Right now, the filter algorithm has to look into the metadata to find the filter criteria. It would be more efficient to use computational down time (after the page loads, while the user is taking in information) to build a richly annotated index of the elements and sort/filter that. Right now, `this.original` is a carbon copy that has to be acted on as any HTMLCollection, but since this is getting so involved there's no reason why I can't build a class with custom getters and setters just to persist and recall the grid data. It would simplify other arms of this octopus to have an API for "here's what objects we can sort".

    console.log("Active filters:")
    console.log(filters)

    for (let i in targets) {
      let entries = Array.from(targets[i].cloneNode(true).children)

      if (filters.length === 0)
        elems.push(entries)
      else
        elems.push(entries.filter(
          (e) => {
            if (e.hasAttribute('data-sorting-metadata')) {
              let meta = JSON.parse(e.getAttribute('data-sorting-metadata'))
              return meta.filters.filter(
                (f) => filters.includes(f)
              ).length
            }
            else
              return false
          }
        ))
    }

    return elems
  }

  update_grid(elems) {
    // TODO: Put logic here to wipe this.gridTarget and replace with the new elements. This function should pay attention to the sort preference and perform sorting if necessary.
    for (let grid in elems) {
      this.gridTargets[grid].querySelectorAll(
        "[data-target='sorting.item']"
      ).forEach( i => i.remove() )
      
      elems[grid].forEach( e => {
        this.gridTargets[grid].appendChild( e.cloneNode(true) )
      })
    }
  }
}
