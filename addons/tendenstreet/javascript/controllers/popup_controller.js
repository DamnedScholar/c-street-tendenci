import { Controller } from "stimulus"

export default class extends Controller {
    static targets = ["display"]

    connect() {
        this.element[this.identifier] = this
        window.popup = this
    }

    show() {
        if (this.data.get("content")) {
            this.displayTarget.innerHTML = this.data.get("content")
            this.displayTarget.classList.remove("hidden")
        }
    }

    hide() {
        this.displayTarget.classList.add("hidden")
    }
}
