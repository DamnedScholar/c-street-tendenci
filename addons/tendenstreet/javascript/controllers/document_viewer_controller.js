import { Controller } from 'stimulus';
// import StimulusReflex from 'stimulus_reflex';

export default class extends Controller {
  initialize() {
    this.element[this.identifier] = this
  }

  connect() {
    // StimulusReflex.register(this)

    // TODO: Based on a list of links passed through HTML, load several iframes into the DOM without displaying them to the user (`visibility: hidden` in CSS; avoid Tailwind since this CSS will be entirely controlled by JS). When each iframe is loaded (https://stackoverflow.com/a/21471494), make a record of its title (if it's an HTML page) and maybe other important information.
  }

  open_viewer() {
    // TODO: Create a lightbox-style modal overlay for the whole window with a panel displaying the requested document (the one in the `href` attribute on the link) and a panel of links to the other URIs passed in the context.
  }
}
