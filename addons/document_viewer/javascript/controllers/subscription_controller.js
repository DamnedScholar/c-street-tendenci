import { Controller } from 'stimulus'
import StimulusReflex from 'stimulus_reflex'

export default class SubscriptionController extends Controller {
    static targets = ['input', 'display']

    connect() {
        this.element[this.identifier] = this
        StimulusReflex.register(this)
    }

    submit (e) {
        e.preventDefault()
        
        this.stimulate('SubscriptionReflex#submit')
            .then(() => this.element.reset())
    }
}
