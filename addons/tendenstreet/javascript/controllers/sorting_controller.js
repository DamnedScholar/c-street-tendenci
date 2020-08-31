import { Controller } from 'stimulus'
// import StimulusReflex from 'stimulus_reflex'
import 'blissfuljs'
import { keepOriginalOrder } from 'webpack/lib/util/comparators'
// import { update } from 'timm'
import voca from 'voca'

// This originally had the attractive name of "Isotope Controller", but there was a namespace conflict with the variable set by the library. Until I come up with a more appealing name, my wrapper will use the banal title "Sorting Controller".

// If this is ever changed, make sure to update category.html, airbnb_list.html, and any tags that use the Sorting version of the name, or else something will definitely break.

export default class extends Controller {
  static targets = [
    'nav', 'cta', 'grid', 'item',
    'categories', 'filters', 'sorts'
  ]

  initialize() {
    this.element[this.identifier] = this
  }

  connect() {
    // StimulusReflex.register(this)

    try {
      this.categories = new Set(this.data.get('categories').split(' '))
    }
    catch {
      this.categories = new Set()
    }
    this.filters = new Set()

    // Take a copy of the server-rendered contents. We will be sorting and filtering from this.
    this.original = this.gridTargets.map(t => t.cloneNode(true))

    if (this.itemTargets) {
      // If we have items, build the nav display.
      this.call_to_action()
      this.add_filters()
    }
  }

  call_to_action() {
    if (this.data.cta) {
      this.navTarget._.inside([
        {
          "tag": "span",
          "className": "",
          "contents": this.data.cta
        }
      ])
    }
  }

  add_filters() {
    // When you click on a feature filter, all feature filter buttons remain visible. When you click on a category filter, all feature filter buttons for hidden items are also hidden and all category filter buttons remain visible.
    console.log("Preparing to add filters.")
    for (item in this.itemTargets) {
      console.log(item)
      filters = item.getAttribute('data-sorting-filters').split(' ')

      this.filters.add(filters)
      console.log("Adding filters " + this.filters.toString)
    }

    if (!this.filters)
      return
      
    buttons = []
    categories = []
    
    for (filter in this.filters) {
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
              "data-action": "click->sorting#filter",
              "data-sorting-filter-button": filter
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
              "data-action": "click->sorting#filter",
              "data-sorting-filter-button": filter
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
      cat_list,
      {
        "tag": "label",
        "className": this.classNames['filter-label'],
        "contents": "Filters:",
        "attributes": {
          "for": "sorting-filters"
        }
      },
      {
        "tag": "ul",
        "id": "sorting-filters",
        "className": this.classNames['filter-list'],
        "contents": buttons,
        "attributes": {
          "data-target": "sorting.filters"
        }
      }
    ])
  }

  add_sorts() {
    // Sorts should never change what appears, only where.

    if (this.filters) {
      buttons = []
      categories = []
      
      for (filter in this.filters) {
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
    button = event.currentTarget
    filterFn = button.getAttribute('name')

    activated = button.toggleAttribute('aria-pressed')
    // If the button was activated, take the current `gridTarget` and filter its children by this button. If it was deactivated, take the original and filter by any buttons still active.
    if (activated) {
      elems = this.run_filters(this.gridTarget, filterFn)
    }
    else {
      active = Array.from(this.filterTarget.children).filter(
        (i) => i.getAttribute('aria-pressed')
        ).map((i) => i.getAttribute('name'))

      elems = this.run_filters(this.original, active)
    }

    this.update_grid(elems)
  }

  run_filters(target, filters) {
    filters = filters.split()   // Make sure this is an array, because it might come in as a string.

    elems = Array.from(target.cloneNode(True).children).filter(
      (i) => {
        i.getAttribute('data-sorting-filters').split().filter(
          (filter) => filters.includes(filter)
        )
      }
    )

    return elems
  }

  update_grid(elems) {
    // TODO: Put logic here to wipe this.gridTarget and replace with the new elements. This function should pay attention to the sort preference and perform sorting if necessary.
    $$('*', this.gridTarget)._.remove()
    
    this.gridTarget._.set({
      "contents": elems
    })
  }
}
