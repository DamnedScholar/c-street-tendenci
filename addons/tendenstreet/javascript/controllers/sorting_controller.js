import { Controller } from 'stimulus'
// import StimulusReflex from 'stimulus_reflex'

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
  }

  sort(e) {
    this.element.activeSort = e.target.value
    // TODO: Finish adding the sort, categorize, and filter actions on the controller. Should ping the console or server with acknowledgement and then instruct the custom element to do its thing.
  }
}
