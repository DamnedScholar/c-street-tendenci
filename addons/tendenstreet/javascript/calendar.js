// Django-Sockpuppet and Stimulus
import { Application } from 'stimulus'
// import StimulusReflex from 'stimulus_reflex'
// import WebsocketConsumer from 'sockpuppet-js'
// import CalendarController from './controllers/calendar_controller'
// import PopupController from './controllers/popup_controller'

import { definitionsFromContext } from "stimulus/webpack-helpers"
const application = Application.start()
const context = require.context("./controllers", true, /\.js$/)
application.load(definitionsFromContext(context))

// const consumer = new WebsocketConsumer('ws://localhost:8000/ws/sockpuppet-sync')

// application.register("calendar", CalendarController)
// application.register("popup", PopupController)
// StimulusReflex.initialize(application, { consumer })

// The library used for the component is Blackstone UI
// import 'blackstone-ui'
// The calendar code is basically Blackstone's, but I copied and pasted it in order to change some style elements.
import './components/cal'

// TODO: The NPM-distributed BUI isn't built for distribution. It doesn't run Parcel on itself before it gets shipped off, so a lot of the modules aren't as easy to get to as they should be and none of the Less is compiled. I should fork the module, compile it, and install my fork, but I can't do that yet because there are guaranteed to be additional steps I can't foresee before it all works perfectly. For now, I'm replacing `b-btn` in the bit of code I've borrowed, but there are enough things I need changed that it's worth sitting down and making a fully-customized fork.
