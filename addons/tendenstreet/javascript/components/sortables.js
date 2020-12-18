import {
  LitElement,
  html,
  css
} from 'lit-element'
import {
  unsafeHTML
} from 'lit-html/directives/unsafe-html.js'
import {
  repeat
} from 'lit-html/directives/repeat.js'

import {Application} from 'stimulus'

import find from 'lodash/find'
import intersection from 'lodash/intersection'
import merge from 'lodash/merge'
import mergeWith from 'lodash/mergeWith'
import sortBy from 'lodash/sortBy'
import xor from 'lodash/xor'
import union from 'lodash/union'

import voca from 'voca'
import Hashids from 'hashids'
import dayjs from 'dayjs'

import {injectStyle} from './utils/styleinjector.js'
import {injectScript} from './utils/scriptinjector.js'

function debug(code="", ...msg) {
  // Pass a series of values or expressions and they will be debugged. Support debug codes for standardized messages and to minimize repetition.

  var announce = "> > > Debugging time!"
  var toBeSent = [announce, ...msg]

  toBeSent.forEach(m=>console.log(m))
}

function error(code="", ...msg) {
  // Pass a series of values or expressions and they will be debugged. Support debug codes for standardized messages and to minimize repetition. Evaluate to `false` to enable return errors.

  var announce = "> > > Error!"
  var toBeSent = [announce, ...msg]

  return (toBeSent.forEach(m=>console.log(m)) && false)
}

export class SortableGrid extends LitElement {
  static get properties() {
    return {
      items: {
        attribute: false
      },
      cats: {
        type: Array,
        reflect: true,
        attribute: 'data-sorting-cats'
      },
      activeCat: {
        type: String,
        attribute: 'data-sorting-active-cat',
        reflect: true
      },
      sorts: {
        type: Array,
        reflect: true,
        attribute: 'data-sorting-sorts'
      },
      activeSort: {
        type: String,
        attribute: 'data-sorting-active-sort',
        reflect: true
      },
      filters: {
        type: Object,
        reflect: true,
        attribute: 'data-sorting-filters'
      },
      activeFilters: {
        type: Object,
        attribute: 'data-sorting-active-filters',
        reflect: true
      }
    }
  }

  // static get styles() {
  //   return css`
  //     :not(grid-items):not(:defined) {
  //       display: block;
  //     }
  //   `
  // }

  constructor() {
    super()

    this.identifier = `sorting`
    console.log(this)

    // We can generate unique hashes by combining the datetime of the page load
    // with the name of the thing being labeled. Preserving Hashids on the
    // object saves work that might be done regenerating it every time we need
    // it, and probably enables stronger persistence with, e.g. Turbolinks since
    // the encoder will last until the object is destroyed and then be renewed
    // with no possibility for overlap.
    this.hashids = new Hashids(dayjs().valueOf().toString())
  }

  async firstUpdated() {
    // `firstUpdated` has to be made async and to wait for the browser's queue to clear to pick up its children, since the browser has to paint in children before they can be recognized.
    super.firstUpdated()

    // TODO: Consider cutting this out into a parent element. Pro: I would be able to rely on `this.childNodes` without thinking about it. Con: I might forget that it's not default behavior.
    await new Promise(r => setTimeout(r,0))
    var items = this.childNodes
    this.items = items

    // Adopt the classes from the grid element to be applied to the new grid element we're creating.
    this.gridClasses = this.getAttribute('class') || ""
    this.removeAttribute('class')

    this.shadowApp = Application.start(this.shadowRoot.firstElementChild)
    // this.shadowApp.start()

    // Save metadata for last since this one calls an update.
    this.digestMetadata(this.items)
  }

  set items(items) {
    // if (!items[0]) // If no content, give up.
    //   return (console.log("Giving up.") && false)
    // TODO: Standardize error messages and present them on a separate property of the custom element. Split off an independent error function that prints the message with annotations for clarity and evaluates falsey, then I only need to return the error function with an error code.

    this._items = Array.from(items).map(e => {
      // `node.nodeType === 1` matches the code for ELEMENT_NODE and ensures
      // that we're not trying to process miscellaneous text nodes.
      if (!(e.nodeType === 1))
        return false

      return e.cloneNode(true)
    })
      .filter(e => e)

    this.requestUpdate()
  }
  get items() {
    if (!this._items)
      return []

    var items = this._items

    const hideIfFalse = (element, tested) => {
      if (tested == false) {
        element.toggleAttribute('hidden', true)
        element.setAttribute('aria-hidden', true)
        element.style.display = "none"
      }
      else {
        // If the element is hidden and we don't have a reason to hide it, show it.
        element.toggleAttribute('hidden', false)
        element.setAttribute('aria-hidden', false)
        element.style.display = ""
      }

      return element
    }

    const tests = (e) => {
      // Eliminating the broadest categories first makes the process more efficient.
      if (!Object.keys(this.activeFilters).length) {
        return true
      }

      try {
        if (!Object.keys(e.sorting).length) {
          return false
        }
      }
      catch {
        // No sorting metadata. We've already established that there are filters active, so we can exclude this.
        return false
      }

      // Categories should exclude everything not of that category. Multiple
      // filters can be applied.
      var catTest = (this.activeCat ?
        (e.sorting.category == this.activeCat) : true)
      
      var filterTest = e.sorting.filters ?
        (
          find(
            Object.keys(this.activeFilters),
            k=>( e.sorting.filters[k]===this.activeFilters[k] )
          ) ? true : false
        ) : false

      return (catTest && filterTest)
    }

    // Whenever we're getting items, we'll do it according to the category,
    // sorts, and/or filters that are active. We can do this by taking the
    // saved Array of items and performing a filter operation, then sorting the
    // remainder.
    var items = this._items
    items = items.map(e => hideIfFalse(e, tests(e)))


    if (this._metadata)
      items = sortBy(items, [i => i.sorting.sorts[this.activeSort]])

    // var output = items.map(e => e.cloneNode(true))

    return items
  }

  set cats(cats) {
    var oldVal = this._cats
    this._cats = cats
    this.requestUpdate("cats", oldVal)

    return this._cats
  }
  get cats() {
    // Build a bar of category buttons.
    return this._cats || []
  }

  set sorts(sorts) {
    var oldVal = this._sorts
    this._sorts = sorts
    this.requestUpdate("sorts", oldVal)

    return this._sorts
  }
  get sorts() {
    // Build a bar of sort buttons.
    return this._sorts || []
  }

  set filters(filters) {
    var oldVal = this._filters
    this._filters = filters
    this.requestUpdate("filters", oldVal)

    return this._filters
  }
  get filters() {
    // Build a bar of filter buttons.
    return this._filters || {}
  }

  set activeCat(cat) {
    if (this.cats.indexOf(cat) != -1)
      this.updateProp("activeCat", cat)
    else
      return (console.log("-> Sortable: Active category must be a valid category.") && false)
  }
  get activeCat() {
    return this._activeCat || ""
  }

  set activeSort(sort) {
    if (this.sorts.indexOf(sort) != -1) // Requested sort must exist.
      if (this._activeSort) // If there is an active sort
        if (this._activeSort === sort) // Toggle off if they match.
          this.updateProp("activeSort", "")
        else
          this.updateProp("activeSort", sort) // Swap active sorts if they don't.
      else
        this.updateProp("activeSort", sort) // Add the sort if none exists.
    else
      return (console.log("-> Sortable: Active sort must be a valid sort.") && false)

    return this._activeSort
  }
  get activeSort() {
    return this._activeSort || ""
  }

  set activeFilters(filter) {
    console.log(`Setting filters:`)
    console.log(filter)
    if (!filter)
      return this._activeFilters = {}

    var filterGroups = Object.keys(this.filters)
    var requested = Object.keys(filter)
    
    const removeEmptyOrNull = (obj) => {
      Object.keys(obj).forEach(k =>
        (obj[k] && typeof obj[k] === 'object') && removeEmptyOrNull(obj[k]) ||
        (!obj[k] && obj[k] !== undefined) && delete obj[k]
      )
      return obj
    }
    
    // The Lodash method `mergeWith()` combines the second object into the first, overwriting any keys that are shared. The custom converter function jumps in and clears the sort value if the values of the shared keys match, allowing for multiple filters to be toggled on/off in a given request. A filter with value `false` won't get counted when the other components are figuring out where they go.
    var existing = this.activeFilters

    mergeWith(existing, filter, (obj,src) => {
      if (obj===src)
        return false
    })

    this._activeFilters = removeEmptyOrNull(existing)

    this.requestUpdate()

    return existing
  }
  get activeFilters() {
    return this._activeFilters || new Object()
  }

  // Utility functions
  updateProp(prop, requested) {
    // This little function DRYs out the updating details. It should not be called before the setter has validated the input.
    var orig = this[prop]
    this[`_${prop}`] = requested
    this.requestUpdate(prop, orig)
    return requested
  }
  digestMetadata(items) {
    var [cats, sorts, filters] = [ [], [], {} ]

    this._metadata = items.map(e => {
      try {
        var metadata = JSON.parse(e.dataset.sortingMetadata)

        if (cats.indexOf(metadata.category) === -1) {
          // Each item only has one category.
          cats.push(metadata.category)
        }
        if (typeof metadata.sorts == "object") {
          Object.keys(metadata.sorts).forEach(sortName => {
            // Each item can have multiple sorts. Sort values are predictable
            // (ascending and descending).
            if (sorts.indexOf(sortName) === -1) {
              sorts.push(sortName)
            }
          })
        }
        if (typeof metadata.filters == "object") {
          Object.keys(metadata.filters).forEach(filterName => {
            // Each item can have multiple filters. Filters are arbitrary.
            mergeWith(
              filters,
              { [filterName]: [metadata.filters[filterName]] },
              (obj=[], src) => {
                return union(obj, src)
              }
            )
          })
        }
      } catch (e) {
        console.log(e)
        // TODO: Replace this error message.
      }

      return metadata
    })
    try {
      this._items.forEach( (v, i, a) => a[i].sorting = this._metadata[i] )
      this._metadata.forEach( (v, i, a) => v.element = this._items[i] )
    } catch {
      console.log("We're missing _items at this stage.")
    }

    // Not calling the setters because we don't want to request three updates.
    this._cats = cats
    this._sorts = sorts
    this._filters = filters

    this.requestUpdate()
  }
  
  hash(value) {
    // The encoding function only accepts numbers, but we're using it to label
    // things identified with human-readable names.
    return this.hashids.encode(value.split('').map(s => s.charCodeAt(0)))
  }

  // Templating functions.
  btnTitle(action, arr) {
    var hash = this.hash(action)

    return html`
      <sortable-interface id="${action}-label-${hash}"
        role="region"
        class="border flex flex-row items-center ml-nudge gap-2"
      >
        <action-title name="${action}"
          role="heading"
          class="text-2xl"
        >
          ${voca.titleCase(action)}
        </action-title>
        <action-interface
          role="navigation" aria-labelledby="${action}-label-${hash}"
          class="flex flex-col gap-1"
        >
          ${ (arr instanceof Array) ?
            this.btnGroup(action, arr) : this.filterGroup(action, arr)}
        </action-interface>
      </sortable-interface>
    `
  }
  filterGroup(action, obj) {
    return html`${repeat( Object.keys(obj), (label, i) => {
      return html`
        <filter-cell name=${label}
          class="flex flex-row gap-2"
        >
          <filter-label class="text-xl italic">
            ${voca.titleCase(label)}
          </filter-label>
          ${this.btnGroup(action, obj[label].sort(), label=label)}
        </filter-cell>
      `
    } )}`
  }
  btnGroup(action, arr, label="") {
    return html`
      <button-block
        class="bg-blue text-gray-100 rounded-lg max-w-max px-3 py-1"
      >
        ${repeat(arr, (btn, i) => {
          var isActive = (
            (action == "categorize" && this.activeCat == btn) ||
            (action == "sort" && this.activeSort == btn) ||
            (action == "filter" && this.activeFilters[label] == btn)
          )

          return html`
            <button @click=${(e) => this[action](e.target)}
              ?active=${isActive} value=${btn} .label=${label}
              class="text-xl border-r-2 last:border-r-0 border-glass-100 border-double px-1"
              >
              ${voca.titleCase(btn)}
            </button>
          `
        } )}
      </button-block>
    `
  }

  // createRenderRoot() {
  //   return this
  // }

  render() {
    var metadata = [
      // [ "categorize", this.cats ],
      [ "sort", this.sorts ],
      [ "filter", this.filters ]
    ]

    return html `
      <content-frame>
        <control-pane class="flex flex-row bg-gray-200 rounded-md w-10/12 p-2 mx-auto border-glass-800 border-2">
          ${injectStyle("tailwind.css")}
          ${repeat(metadata, i=>html`${this.btnTitle(i[0],i[1])}`)}
        </control-pane>
        <grid-items id="grid-${this.hash("grid")}" class=${this.gridClasses}
          role="article">
          ${repeat(this.items, i=>i.id, i=>html`${i}`)}
        </grid-items>
        <slot hidden></slot>
      </content-frame>
    `
  }

  // These are the actions that can be taken.
  categorize(btn) {
    // TODO: Add validation to make sure category is a string.
    var query = btn.value
    this.activeCat = query
  }
  sort(btn) {
    // TODO: Add validation to make sure sort is a string.
    console.log("Sorted.")
    var query = btn.value
    this.activeSort = query
  }
  filter(btn) {
    // TODO: Add validation to make sure filter is an object.
    console.log("Filtered.")
    var query = new Object()
    query[btn.label] = btn.value
    console.log(query)
    this.activeFilters = query
  }
}
