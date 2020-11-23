import {html, render} from 'https://unpkg.com/lit-html?module'
import {LitElement, property, css} from 'https://unpkg.com/lit-element?module'
import {styleMap} from 'https://unpkg.com/lit-html/directives/style-map.js?module'
import {classMap} from 'https://unpkg.com/lit-html/directives/class-map.js?module'

import device from 'blackstone-ui/util/device.js'
import {injectStyle} from './utils/styleinjector.js'

export default class extends LitElement{
  static get styles(){return css`
      b-btn::not([active]) {
          opacity: 0.6;
      }
  `}

  render(){return html`
    ${injectStyle("tailwind.css")}
    <slot name="menu:before"></slot>

    ${this.views.map(v=>html`
        ${v.canDisplay&&(!device.isMobile||v.id!='emails')?html`
            <b-btn text icon="${v.icon}" ?active=${v.active} .tabView=${v} @click=${this.onClick}>
                <span class="text-2x">${v.title}</span>
            </b-btn>
        `:''}
    `)}
    <div>
      ${this.forward}
      ${this.back}
    </div>

    ${this.shouldShowSearch?html`
        <b-btn text stacked icon="search" @click=${this.focusSearch}>
            <span>Search</span>
        </b-btn>
    `:''}

    <slot name="menu:after"></slot>
  `}

  get forward(){return html`
    <b-btn>
      <span>Forward</span>
    </b-btn>  
  `}

  get back(){return html`
    <b-btn>
      <span>Back</span>
    </b-btn>  
  `}

  get shouldShowSearch(){
    return device.isMobile
  }

  focusSearch(){
      window.dispatchEvent(new Event('focus-search'))
  }

  onClick(e){
      this.onMenuClick(e)
  }
}
