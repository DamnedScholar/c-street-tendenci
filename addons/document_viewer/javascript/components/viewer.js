import {html, render} from 'https://unpkg.com/lit-html?module'
import {LitElement, html as ehtml, property, css} from 'https://unpkg.com/lit-element?module'
import {styleMap} from 'https://unpkg.com/lit-html/directives/style-map.js?module'

import {injectStyle} from './utils/styleinjector.js'

import ResponsiveTabBar from './tabs.js'

export default class extends LitElement {
    static get properties() { return {
      // Trigger a redraw of the element if any of these building block properties change.
      item: {attribute: false},
      loading: {attribute: false},
      css: {attribute: false}
    }}
  
    @property({attribute: true, type: String, reflect: true})
    current = ''
    @property({attribute: true, type: Array, reflect: true})
    links = []
  
    constructor() {
      super()
  
      // Set defaults. Nothing dynamic should go here.
      this.sniffers = []
  
      this.loading = ehtml`
        Loading...
      `
  
      this.css = {
        viewer: {
          "height": "100%",
          "display": "flex",
          "flex-direction": "column-reverse"
        },
        // grid: {
          // TODO: Prototyping for a potential grid version.
          // "display": "grid",
          // "grid-template-areas": `
          //   "topbar topbar"
          //   "tabs body"
          //   "sidebar body"
          // `,
        // },
        tabs: {
          "height": "100%"
        },
        frame: {
          "height": "100%",
          "width": "100%"
        },
        topbar: {
          "height": "100px",
          "display": "flex",
          "justify-content": "space-around"
        }
      }
  
      // TODO: I can make forward/back buttons in b-ui's tab bar using the `.views` property (https://github.com/kjantzer/bui/blob/master/presenters/tabs/index.js#L83) and `tab_bar.views.active` with `tab_bar.views.at(active + 1)` or `(active - 1)`. I need to bind these to hotkeys using `stimulus-hotkeys` and to buttons that appear on mobile devices.
  
      customElements.define('responsive-tab-bar', ResponsiveTabBar)
    }
  
    updateTab(evt) {
      var view = evt.target.parentElement

      // Save a reference to each sniffer for later.
      this.sniffers.push( setInterval( (view) => {
        var id = view.tabView.id
        var tabBar = this.content
        var hasCustomTabBar = tabBar.getAttribute('tab-bar')

        tabBar = hasCustomTabBar ?
          tabBar.shadowRoot.querySelector(hasCustomTabBar).shadowRoot.querySelector('.tab-bar') :
          tabBar.shadowRoot.querySelector('.tab-bar')
        
        console.log(`Sniffing at ${tabBar.querySelector(id)}`)
        var tab = tabBar.querySelector(id)
  
        try {
          tab.textContent = view.contentDocument.title.replace(this.croptitle, "")
        }
        catch {
          // Do nothing.
        }
        
      }, 100, view) )
    }
  
    clone(node) {
      var newNode = node.cloneNode(true)
    }
  
    render() {
      this.item = (link, id) => ehtml`
        <section title="Loading..." view-id="view-${id}">
          <iframe style="${styleMap(this.css.frame)}" src="${link}" frameborder="0"
            @load="${ (evt) => this.updateTab(evt) }"
          ></iframe>
        </section>
      `
  
      let hotkeys = {
        "left": "[data-controller='document-viewer']->document_viewer#back",
        "right": "[data-controller='document-viewer']->document_viewer#forward",
      }

      let display = ehtml`
        ${injectStyle("tailwind.css")}
        <viewer style=${styleMap(this.css.viewer)}
          data-controller="hotkeys"
          data-hotkeys-bindings-value='${JSON.stringify(hotkeys)}'>
          <b-tabs tab-bar="responsive-tab-bar" layout="left"
            style=${styleMap(this.css.tabs)}>
            ${this.links.map( (v, i) => {
              var view = this.item(v, i)

              Object.assign(view, {
                'title': this.loading,
                'id': i,
                'url': v
              })

              return view
            } )}
          </b-tabs>
          <topbar style=${styleMap(this.css.topbar)}>
            ${this.controller.topbarTargets.map( (t) => {
              var newNode = t.cloneNode(true)
  
              return newNode
            } )}
          </topbar>
        </viewer>
      `
  
      return ehtml`${display}`
    }
  
    // Build an API for the different organs of this component.
    //    viewer -> The top-level wrapper.
    //    views -> Nodelist of all views
    //    sidebar -> Element containing the sidebar content.
    //    topbar -> Element containing the topbar content.
    get viewer() {
      return this.shadowRoot.querySelector('viewer')
    }
  
    get content() {
      return this.shadowRoot.querySelector('b-tabs')
    }
  
    get sidebar() {
      return this.shadowRoot.querySelector('sidebar')
    }
  
    get topbar() {
      return this.shadowRoot.querySelector('topbar')
    }
  
    get keys() {
      // Return an array of all tab names.
      return Array.from(this.content.views.keys())
    }
  
    get active() {
      return this.content.active
    }
  
    set active(view) {
      this.content.active = view
    }
  
    forward() {
      var len = this.keys.length
      var target = this.keys.indexOf(this.active) + 1
      this.active = this.keys[target%len]
    }
  
    back() {
      var len = this.keys.length
      var target = this.keys.indexOf(this.active) + len - 1
      this.active = this.keys[target%len]
    }
  }
