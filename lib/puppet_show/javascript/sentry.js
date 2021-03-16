import { Application } from 'stimulus'
// import StimulusReflex from 'stimulus_reflex'
// import WebsocketConsumer from 'sockpuppet-js'
import SentryController from './controllers/sentry_controller'


const application = Application.start()
// const consumer = new WebsocketConsumer('ws://localhost:8000/ws/sockpuppet-sync')

application.register("sentry", SentryController)
// StimulusReflex.initialize(application, { consumer })
