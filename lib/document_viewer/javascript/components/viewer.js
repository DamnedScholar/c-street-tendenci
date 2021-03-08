import {LitElement, html, css} from 'lit-element'
import {styleMap} from 'lit-html/directives/style-map.js'

import {injectStyle} from './utils/styleinjector.js'

import ResponsiveTabBar from './tabs.js'

export default class extends LitElement {
    static get properties() { return {
      item: {attribute: false},
      loading: {attribute: false},
      retainedHeight: {attribute: false},
      links: {
        attribute: 'data-document_viewer-links-value',
        type: Array,
        reflect: true
      },
      current: {
        attribute: 'data-document_viewer-current-value',
        type: String,
        reflect: true
      },
      croptitle: {
        attribute: 'data-document_viewer-croptitle-value',
        type: String,
        reflect: true
      }
    }}
  
    constructor() {
      super()
  
      // Set defaults. Nothing dynamic should go here.
      this.sniffers = []

      this.retainedHeight = "0px"
  
      this.loading = `Loading...`
  
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
      var doc = evt.path[0]
      var parent = evt.path[3]

      // Save a reference to each sniffer for later.
      this.sniffers.push( setInterval( (doc, parent) => {
        var id = doc.tabView.id
        var tab = parent.querySelector(`[slot="menu:${id}"]`)
  
        try {
          tab.textContent = doc.contentDocument.title.replace(
            this.croptitle, "")

          var bodyHeight = getComputedStyle(doc.contentDocument.body)['height']
          if (
            bodyHeight != "auto" &&
            bodyHeight != "0px" &&
            bodyHeight != this.retainedHeight
          )
            this.retainedHeight = bodyHeight

          this.content.update()
        }
        catch (e) {
          console.log(e)
          // Do nothing.
        }
        
      }, 100, doc, parent) )
    }
  
    clone(node) {
      var newNode = node.cloneNode(true)
    }

    item (link, id, title) {
      return html`
        <iframe title="view-${id}"
          class="h-screen w-full" style=${styleMap({height: this.retainedHeight})}
          src=${link} frameborder="0"
          @load=${ this.updateTab }
        ></iframe>
        <span slot="menu:view-${id}">${title}</span>
      `
    }
  
    render() {
      let hotkeys = {
        "left": "[data-controller='document-viewer']->document_viewer#back",
        "right": "[data-controller='document-viewer']->document_viewer#forward",
      }

      let display = html`
        ${injectStyle("tailwind.css")}
        <viewer-window style=${styleMap(this.css.viewer)}
          data-controller="hotkeys"
          data-hotkeys-bindings-value='${JSON.stringify(hotkeys)}'>
          <b-tabs old-tab-bar="responsive-tab-bar" layout="left"
            style=${styleMap(this.css.tabs)}
          >
            ${this.links.map( (v, i) => {
              var title = this.loading
              var view = this.item(v, i, title)
      
              Object.assign(view, {
                'title': title,
                'id': i,
                'url': v
              })
      
              return view
            } )}
          </b-tabs>
          <viewer-topbar>
            <slot name="topbar"></slot>
          </viewer-topbar>
        </viewer-window>
      `
  
      return html`${display}`
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
