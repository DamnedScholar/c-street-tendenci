import { Controller } from 'stimulus';
import StimulusReflex from 'stimulus_reflex';

export default class extends Controller {
  // static targets = ['tag-filter', 'grid', 'listing']

  // initialize() {
  //   this.element['isotope'] = this
    
  //   this.iso = new Isotope( '.grid', {
  //     itemSelector: '.element-item',
  //     layoutMode: 'fitRows'
  //   });
  // }

  // connect() {
  //   StimulusReflex.register(this)
  // }

  // filter(event) {
  //   filterFn = event.currentTarget.getAttribute('data-filter')

  //   this.iso.arrange({
  //     filter: this[filterFn](event)
  //   })
  // }

  // filterTags(event) {
  //   var taglist = this.gridTarget.querySelector('.tags').innerText
  //   tag = new RegExp(event.target.innerText)
  //   return taglist.match( tag )
  // }

  // filterOpen(status) {
  //   var status = itemElem.querySelector('.status').innerText
  //   return status.match( /open/ )
  // }

  // filterService(service) {
  //   this.iso.arrange({
  //     // item element provided as argument
  //     filter: function( itemElem ) {
  //       var service = itemElem.querySelector('.tags').innerText
  //       return service.match( /ium$/ )
  //     }
  //   })
  // }
}
