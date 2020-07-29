import { LitElement, html, css } from 'lit-element'
import 'blackstone-ui/elements/btn-group'
import 'blackstone-ui/helpers/lit-element/events'
import moment from 'moment'

// TODO: The fastest version of this might be to rely on the server to tell me the date and use Sockpuppet and Stimulus for monthly navigation. Since I'm overriding the component, it wouldn't necessarily be a huge step.

customElements.define('b-cal', class extends LitElement{

    constructor(){
        super()

        this.weekdays = moment.weekdaysMin()

        this.days = new Array(7*6).fill('')
        this.date = this._date || this.getAttribute('date') || moment()
    }

    static get styles(){return css`
        :host {
            /* height: 100%; */
            display: grid;
            position:relative;
            display: grid;
            grid-template-rows: auto 1fr;
            --grid-cols: 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
        }
        :host([collapse-weekend]) {
            --grid-cols: 2.5em 1fr 1fr 1fr 1fr 1fr 2.5em;
        }
        header {
            position: sticky;
            top: 0;
            z-index: 10;
            background: var(--b-cal-header-bgd, var(--theme-bgd, #fff));
            border-bottom: solid 1px rgba(var(--theme-rgb, 0,0,0), .1);
            display: grid;
            grid-template-columns: max-content max-content;
            justify-content: space-between;
            align-items: center;
            padding: .75em 1em 0;
        }
        header .title,
        header .nav {
            display: flex;
            align-items: center;
        }
        h1, h2, h3 {
            margin: 0;
        }
        .weekdays {
            margin: .75em -1em 0;
            grid-column: 1/-1;
            display: grid;
            grid-template-columns: var(--grid-cols);
            text-align: right;
        }
        .weekdays > div {
            padding-right: .75em;
            padding-bottom: .5em;
        }
        main {
            /* height: 100%; */
            display: grid;
            position:relative;
            display: grid;
            grid-template-columns: var(--grid-cols);
            grid-template-rows: repeat(6, 1fr);
            gap: 1px;
            /* min-height: 0; */
        }
        b-cal-day {
            border-right: solid 1px rgba(var(--theme-rgb, 0,0,0), .1);
            border-bottom: solid 1px rgba(var(--theme-rgb, 0,0,0), .1);
            flex-shrink: 0;
            min-width: 0;
        }
        b-cal-day[weekend] {
            background: var(--theme-bgd-accent, #f5f5f5);
        }
    `}

    get date(){ return this._date }

    set date(val){
        
        let oldDate = this._date && this._date.clone()

        if( val instanceof moment ){
            this._date = val
			this._dateSelected = this._date.clone()

        }else if( typeof val == 'string' ){

            this._date = moment(val)
			this._dateSelected = this._date.clone()

		}else if( val && typeof val == 'object' ){
			this._dateSelected.set(val)
			this._date.set(val)
        }

		this._date.set({date: 1})

        if( oldDate && this._date.isSame(oldDate) )
            return

        this._loadDays()

        this.emitEvent('date-changed', this.range)
	}

    firstUpdated(){
        this.emitEvent('date-changed', this.range)
    }

    _loadDays(){
        let start = this._date.weekday()
		let numDays = this._date.daysInMonth()

        this.days = this.days.map((_, i)=>{
            return this._date.clone().add(i-start, 'day')
        })
    }

    get range(){
        return [this.days[0], this.days[this.days.length-1]]
    }

    nextMonth(){
		this.date = this._date.clone().add('month', 1)
        this.update()
	}

	prevMonth(){
		this.date = this._date.clone().add('month', -1)
        this.update()
	}

    goToToday(){
        this.date = moment()
        this.update()
    }

    render(){return html`
        <header>
            <div class="title">
                <h1>${this.date.format('MMMM YYYY')}</h1>
                <slot name="after-title"></slot>
            </div>
            <div class="nav">
                <slot name="before-nav"></slot>
                <div style="color:#2d4066; font-size:1.25rem;">
                    <b-btn text icon="fad fa-chevron-left" @click=${this.prevMonth}>
                        <svg aria-hidden="true" focusable="false" data-prefix="fad" data-icon="chevron-square-left" class="svg-inline--fa fa-chevron-square-left fa-w-14" style="width:18px;" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><g class="fa-group"><path class="fa-secondary" fill="currentColor" d="M400 32H48A48 48 0 0 0 0 80v352a48 48 0 0 0 48 48h352a48 48 0 0 0 48-48V80a48 48 0 0 0-48-48zm-95.51 325.57a24 24 0 0 1 0 33.95l-17 17a24 24 0 0 1-33.95 0L118.06 273a24 24 0 0 1 0-33.94l135.51-135.54a24 24 0 0 1 33.95 0l17 17a24 24 0 0 1 0 33.94L202.91 256z" opacity="0.4"></path><path class="fa-primary" fill="currentColor" d="M118.06 239l135.51-135.48a24 24 0 0 1 33.95 0l17 17a24 24 0 0 1 0 33.94L202.91 256l101.58 101.57a24 24 0 0 1 0 33.95l-17 17a24 24 0 0 1-33.95 0L118.06 273a24 24 0 0 1 0-34z"></path></g></svg>
                    </b-btn>
                    <b-btn text @click=${this.goToToday} style="color:#2d5c66">Today</b-btn>
                    <b-btn text icon="fad fa-chevron-right" @click=${this.nextMonth}>
                        <svg aria-hidden="true" focusable="false" data-prefix="fad" data-icon="chevron-square-right" class="svg-inline--fa fa-chevron-square-right fa-w-14" style="width:18px;" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><g class="fa-group"><path class="fa-secondary" fill="currentColor" d="M400 32H48A48 48 0 0 0 0 80v352a48 48 0 0 0 48 48h352a48 48 0 0 0 48-48V80a48 48 0 0 0-48-48zm-70.06 241L194.43 408.48a24 24 0 0 1-33.94 0l-17-17a24 24 0 0 1 0-33.94L245.09 256 143.52 154.43a24 24 0 0 1 0-33.94l17-17a24 24 0 0 1 33.94 0L329.94 239a24 24 0 0 1 0 34z" opacity="0.4"></path><path class="fa-primary" fill="currentColor" d="M143.52 154.43a24 24 0 0 1 0-33.94l17-17a24 24 0 0 1 33.94 0L329.94 239a24 24 0 0 1 0 33.94L194.43 408.48a24 24 0 0 1-33.94 0l-17-17a24 24 0 0 1 0-33.94L245.09 256z"></path></g></svg>
                    </b-btn>
                </div>
                <slot name="after-nav"></slot>
            </div>
            <div class="weekdays">${this.weekdays.map((str,i)=>html`
                ${i==0||i==6?html`
                    <div @click=${this.toggleCollapseWeekend}>${str}</div>
                `:html`
                    <div>${str}</div>
                `}
            `)}</div>
        </header>
        <main>
        ${this.days.map(date=>html`
            <b-cal-day .caldate=${this._date} .date=${date}>
                <slot name="${date.format('YYYY-MM-DD')}"></slot>
            </b-cal-day>
        `)}
        </main>
    `}

    toggleCollapseWeekend(){
        this.toggleAttribute('collapse-weekend', !this.hasAttribute('collapse-weekend'))
    }

})

customElements.define('b-cal-day', class extends LitElement{

    static get styles(){return css`
        :host {
            display: grid;
            grid-template-rows: auto 1fr;
            overflow: visible;
            padding: .25em;
        }
        header {
            text-align: right;
        }
        main {
            overflow: visible;
        }
        .date {
            height: 1.8em;
            min-width: 1.8em;
            box-sizing: border-box;
            display: inline-flex;
            justify-content: center;
            align-items: center;
            border-radius: 1em;
        }
        :host([overflow]) .date {
            color: var(--theme-color-accent, #999);
            padding: 0 .35em;
        }
        :host([today]) .date {
            color: #fff;
            background: var(--theme, var(--blue, #2196F3));
        }
    `}

    get isOverflow(){
        return this.caldate.month() != this.date.month()
    }

    get isWeekend(){
        return [0, 6].includes(this.date.weekday())
    }

    get isToday(){
        return this.date.isSame(new Date(), 'day')
    }

    render(){return html`
        <header>
            <div class="date">
                ${this.date.date()==1?this.date.format('MMM'):''}
                ${this.date.get('date')}
            </div>
        </header>
        <main>
            <slot></slot>
        </main>
    `}

    set date(date){
        this.__date = date

        this.toggleAttribute('weekend', this.isWeekend)
        this.toggleAttribute('overflow', this.isOverflow)
        this.toggleAttribute('today', this.isToday)

        this.requestUpdate()
    }

    get date(){
        return this.__date
    }

    // firstUpdated(){
    //     let slot = this.shadowRoot.querySelector('slot');
    //     this.main = this.shadowRoot.querySelector('main');
    //     slot.addEventListener('slotchange', this.onSlotChange.bind(this));
    // }

    // onSlotChange(e){
    //     let nodes = e.target.assignedNodes();

    //     if( nodes[0] && nodes[0].nodeName == '#text' )
    //         return

    //     let doesOverflow = this.main.offsetHeight < this.main.scrollHeight

    //     console.log(doesOverflow);
    // }

})

export default class BtnElement extends LitElement {

    static get properties() { return {
        href: {type: String, reflect: true},
        value: {type: String, reflect: true},
        icon: { type: String },
        spin: {type: Boolean, reflect: true, attribute: 'spin'}
    }}

    static get styles(){ return css`
    
        :host{
            --red: var(--red-700);
            /* --black: #333;
            --orange: #F57C00;
            --blue: #2196F3;
            --red: #d32f2f;
            --gray: #444444;
            --green: #27ae60;
            --yellow: #f2d57e;
            --teal: #009688;
            --purple: #7E57C2;
            --brown: #795548;
            --pink: #E91E63; */
            --radius: 3px;
            --color: var(--b-btn-bgd, var(--black)) ;
            --bgdColor: var(--color);
            --hoverBgdColor: rgba(255,255,255,.1);
            --textColor: var(--b-btn-color, #fff);
            --borderColor: var(--color);
            --borderStyle: solid;
            --borderWidth: 1px;
            --padding: .4em .6em;
            display: inline-grid;
            position: relative;
            box-sizing: border-box;
            background: var(--bgdColor);
            color: var(--textColor);
            border-radius: var(--radius);
            cursor: pointer;
            transition: 
                color 160ms,
                background-color 160ms,
                border 160ms;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            text-rendering: optimizeLegibility;
            font-size: .9rem;
            line-height: 1rem;
            font-weight: bold;
            font-family: var(--bui-btn-font);
            -webkit-touch-callout: none; /* iOS Safari */
            -webkit-user-select: none; /* Safari */
            -khtml-user-select: none; /* Konqueror HTML */
            -moz-user-select: none; /* Firefox */
            -ms-user-select: none; /* Internet Explorer/Edge */
            user-select: none; 
        }
        /* hide by default */
        @media print {
            :host {
                display: none;
            }
        }
        :host([hidden]) {
            display: none !important;
        }
        main {
            border-radius: var(--radius);
            position: relative;
            display: inline-flex;
            justify-content: center;
            align-items: center;
            padding: var(--padding);
            box-sizing: border-box;
            /*padding-bottom: .3em;*/ /* remove descender line to make it look more centered*/
            text-overflow: ellipsis;
            border: var(--borderStyle) var(--borderWidth) var(--borderColor);
            /* transition: 120ms; */
        }
        main > span {
            display: inline-flex;
            justify-content: center;
        }
        slot {
            display: block;
            margin-bottom: -.1em; /* remove descender line to make it look more centered*/
        }
        slot::slotted(*) {
            display: inline-block;
            margin-top: 0;
            margin-bottom: 0;
        }
        .hover {
            position: absolute;
            display: block;
            width: 100%;
            height: 100%;
            left: 0;
            top: 0;
            background: var(--hoverBgdColor);
            visibility: hidden;
            opacity: 0;
            /* mix-blend-mode: saturation; */
            border-radius: var(--radius);
            /* transition: 120ms; */
        }
        @media (hover) {
            :host(:hover) .hover {
                opacity: 1;
                visibility: visible;
            }
        }
        /* b-icon,
        ::slotted(b-icon) {
            vertical-align: bottom;
        } */
        b-spinner {
            opacity: 0;
            visibility: hidden;
            --size: 1em;
            margin-left: -1.35em;
            margin-right: .35em;
            transition: 120ms;
        }
        :host([spin]) b-spinner {
            opacity: 1;
            visibility: visible;
            margin-left: 0;
        }
        :host([spin]) b-icon {
            display: none;
        }
        main b-icon {
            margin-right: .35em;
            margin-left: -.15em;
        }
        :host([stacked]) {
            --padding: .3em .5em .1em .5em;
        }
        :host([stacked]) main {
            display: inline-grid;
            align-content: center;
        }
        :host([stacked]) b-icon {
            font-size: 1.2em;
            margin: 0;
        }
        :host([stacked]) slot {
            font-size: .6em;
        }
        :host([stacked]) slot::slotted(*) {
            opacity: var(--b-btn-stacked-label-opacity, .5);
        }
        :host([stacked]) slot[name="icon"] {
            font-size: 1em;
            display: contents;
        }
        :host([stacked]) slot[name="icon"]::slotted(*),
        :host([stacked]) slot[name="icon"] b-icon{
            opacity: var(--b-btn-stacked-icon-opacity, 1);
        }
        :host([stacked]) b-spinner {
            font-size: 1.2em;
            margin-right: 0;
            margin-left: -1em;
        }
        :host([stacked][spin]) b-spinner {
            margin-left: 0;
        }
        :host([block]) {
            display: block;
            text-align: center
        }
        :host([block]) main {
            display: flex;
            justify-content: center
        }
        :host(:empty) main {
            --padding: .4em .5em;
        }
        :host(:empty) main b-icon {
            margin-left: 0;
            margin-right: 0;
        }
        /* offset play icon to make it appear more centered */
        :host(:empty) main b-icon[name="play"] {
			margin: 0 -.1em 0 .1em;
        }
        :host([color^="primary"])  { --color: var(--color-primary); }
        :host([color^="theme"])  { --color: var(--theme); }
        :host([color^="black"])  { --color: var(--black); }
        :host([color^="white"])  { --color: var(--white); --textColor: var(--black); }
        :host([color^="orange"]) { --color: var(--orange); }
        :host([color^="blue"])   { --color: var(--blue); }
        :host([color^="red"])    { --color: var(--red); }
        :host([color^="gray"])   { --color: var(--gray); }
        :host([color^="green"])  { --color: var(--green); }
        :host([color^="yellow"]) { --color: var(--yellow); }
        :host([color^="teal"])   { --color: var(--teal); }
        :host([color^="purple"]) { --color: var(--purple); }
        :host([color^="brown"])  { --color: var(--brown); }
        :host([color^="pink"])   { --color: var(--pink); }
        @media (hover){
        :host([color*="hover-black"]:hover)  { --color: var(--black); }
        :host([color*="hover-orange"]:hover) { --color: var(--orange); }
        :host([color*="hover-blue"]:hover)   { --color: var(--blue); }
        :host([color*="hover-red"]:hover)    { --color: var(--red); }
        :host([color*="hover-gray"]:hover)   { --color: var(--gray); }
        :host([color*="hover-green"]:hover)  { --color: var(--green); }
        :host([color*="hover-yellow"]:hover) { --color: var(--yellow); }
        :host([color*="hover-teal"]:hover)   { --color: var(--teal); }
        :host([color*="hover-purple"]:hover) { --color: var(--purple); }
        :host([color*="hover-brown"]:hover)  { --color: var(--brown); }
        :host([color*="hover-pink"]:hover)   { --color: var(--pink); }
        }
        :host([pill]) {
            --radius: 1em;
        }
        /* @media (hover) { */
        :host([outline]:not(:hover)) {
            --bgdColor: transparent;
            --textColor: var(--color);
        }
        /* } */
        /* :host([outline]:hover){
            --bgdColor: var(--color);
            --textColor: inherit;
        } */
        :host([text]),
        :host([clear]) {
            --bgdColor: transparent;
            --textColor: var(--color);
            --borderColor: transparent;
        }
        /* :host([text]) .hover,
        :host([clear]) .hover {
            display: none;
        } */
        :host([text]) {
            font-size: 1em;
            font-weight: normal;
        }
        @media (hover){
        :host([text]:hover),
        :host([clear]:hover) {
            --bgdColor: rgba(0,0,0,.05);
        }}
        :host([text].popover-open),
        :host([clear].popover-open) {
            --bgdColor: rgba(0,0,0,.05);
        }
        :host([xs]) { font-size: .6rem; }
        :host([sm]) { font-size: .8rem; }
        :host([lg]) { font-size: 1.2rem; }
        :host([xl]) { font-size: 1.4rem; }
        /* floating action btn */
        :host([fab]) {
            position: absolute;
            z-index: 100;
            box-shadow: 0px 3px 5px -1px rgba(0,0,0,0.2),
                        0px 6px 10px 0px rgba(0,0,0,0.14),
                        0px 1px 18px 0px rgba(0,0,0,0.12);
            bottom: 1rem;
            right: 1rem;
            font-size: 1.4em;
            width: 2em;
            height: 2em;
            --radius: 2em;
            overflow: hidden;
        }
        :host([fab]) b-spinner {
            margin-right: 0;
            margin-left: -1em;
        }
        :host([fab][spin]) b-spinner {
            margin-left: 0;
        }
    `}

    // TODO: This version replaces `b-icon` with FA icons as a quick compatibility fix. If I fully customize BUI, I might want to make it know about FA on its own.

    render(){ return html`
        <div class="hover"></div>
        <main>
            <span>
                <b-spinner></b-spinner>
                <slot name="icon">
                    ${this.icon?html`<i class="${this.icon}"></i>`:''}
                </slot>
            </span>
            <slot></slot>
        </main>
    `}

	constructor(){
		super()
        this.icon = ''
        this.spin = false
	}

    firstUpdated(){
        this.addEventListener('click', ()=>{
            if( this.href )
                window.location = this.href
        }, true)
    }

}

customElements.define('b-btn', BtnElement)

/*
	SVG and idea taken from https://ant.design/components/button/
	
	Examples: 
	<circle-spinner/>
	<circle-spinner style="--size:.8em; color: white"/>
*/

class SpinnerElement extends HTMLElement {
	
    constructor() {
        super()
		
        let shadow = this.attachShadow({mode: 'open'})
        let temp = document.createElement('template')
        
        temp.innerHTML = `<style>
			:host {
				--size: .8em;
				height: var(--size);
			    width: var(--size);
			    display: inline-block;
			    vertical-align: middle;
			}
			
			:host(.overlay) {
				position: absolute;
				top: 50%;
				left: 50%;
				transform: translate(-50%, -50%);
				z-index: 10000;
			}
			
			@keyframes spin {
				100% {
				    transform: rotate(360deg);
				}
			}
			
			svg {
				animation: spin 1s infinite linear;
				transform-origin: center center;
			}
			</style>
			<svg viewBox="0 0 1024 1024" class="spin" data-icon="loading" width="100%" height="100%" fill="currentColor" aria-hidden="true">
				<path d="M988 548c-19.9 0-36-16.1-36-36 0-59.4-11.6-117-34.6-171.3a440.45 440.45 0 0 0-94.3-139.9 437.71 437.71 0 0 0-139.9-94.3C629 83.6 571.4 72 512 72c-19.9 0-36-16.1-36-36s16.1-36 36-36c69.1 0 136.2 13.5 199.3 40.3C772.3 66 827 103 874 150c47 47 83.9 101.8 109.7 162.7 26.7 63.1 40.2 130.2 40.2 199.3.1 19.9-16 36-35.9 36z"></path>
			</svg>`
			
        this.shadowRoot.appendChild(temp.content.cloneNode(true));
    }
}

customElements.define('b-spinner', SpinnerElement)

export default customElements.get('b-cal')
