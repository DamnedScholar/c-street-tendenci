import { Controller } from 'stimulus'
import StimulusReflex from 'stimulus_reflex'

export default class SubscriptionController extends Controller {
    static targets = ['input']

    connect() {
        this.element[this.identifier] = this
        StimulusReflex.register(this)
    }

    submit (e) {
        e.preventDefault()
        
        this.stimulate('SubscriptionReflex#submit')
            .then(() => {
                this.element.reset()
                // optional: set focus on the freshly cleared input
                this.inputTarget.focus()
            })
            .catch(payload => console.log(payload))
    }

    beforeSubmit() {
        console.log("Do we win?")
    }

    submitSuccess() {
        console.log("We win!")
    }
}
