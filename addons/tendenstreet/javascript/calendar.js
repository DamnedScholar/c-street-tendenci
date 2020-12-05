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
import 'blackstone-ui/presenters/cal/index.js'
