import { Controller } from 'stimulus'
import StimulusReflex from 'stimulus_reflex'

export default class SubscriptionController extends Controller {
    static targets = ['input']

    connect() {
        this.element[this.identifier] = this
        StimulusReflex.register(this)
    }

    submit() {
        var email = this.inputTarget.value

        this.stimulate('SubscriptionReflex#submit', this.inputTarget, email)
    }
}
