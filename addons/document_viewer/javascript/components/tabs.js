import {render} from 'https://unpkg.com/lit-html?module'
import {LitElement, html, css} from 'https://unpkg.com/lit-element?module'
import {styleMap} from 'https://unpkg.com/lit-html/directives/style-map.js?module'
import {classMap} from 'https://unpkg.com/lit-html/directives/class-map.js?module'

import device from 'blackstone-ui/util/device.js'
import {injectStyle} from './utils/styleinjector.js'

export default class extends LitElement{
  static get styles() { return css`
      b-btn::not([active]) {
          opacity: 0.6;
      }
  `}

  get tabBar() {
    return html`
      <header class="tab-bar" part="tab-bar">
        <slot name="menu:before"></slot>
        ${this.collapsed}
        ${this.views.map(v=>this.renderTab(v))}
        <slot name="menu:after"></slot>
      </header>
      `
  }

  get collapsed() {
    return device.isMobile ?
      html`
        <div class="tab-bar-item single-menu" active @click=${this.popoverMenu}>
          <b-icon name="menu"></b-icon>
          ${this.views.active.title}
        </div>
      ` :
      html``
  }

  renderTab(v) {
    return html`
      ${v.canDisplay&&(!device.isMobile||v.id!='emails')?html`
        <btn text id="${v.id}"
          icon="${v.icon}" ?active=${v.active}
          .tabView=${v} @click=${this.menuClick}>
          <span class="text-2x">
            ${v.title}
          </span>
        </btn>
      `:''}
    `
  }

  get forward() { return html`
    <button data-action="document-viewer#forward">
      Forward
    </button>
  `}

  get back() { return html`
    <button data-action="document-viewer#back">
      Back
    </button>
  `}

  get shouldShowSearch() {
    return false
    // return device.isMobile
  }

  focusSearch() {
      window.dispatchEvent(new Event('focus-search'))
  }

  onClick(e) {
      this.onMenuClick(e)
  }

  render() { return html`
    ${injectStyle("tailwind.css")}
    <slot name="menu:before"></slot>

    ${this.tabBar}

    ${this.shouldShowSearch?html`
        <b-btn text stacked icon="search" @click=${this.focusSearch}>
            <span>Search</span>
        </b-btn>
    `:''}

    <slot name="menu:after"></slot>
  `}
}
