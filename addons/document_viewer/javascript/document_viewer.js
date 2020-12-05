import { Application } from 'stimulus'
import StimulusReflex from 'stimulus_reflex'
import WebsocketConsumer from 'sockpuppet-js'

const application = Application.start()
const consumer = new WebsocketConsumer('ws://localhost:8000/ws/sockpuppet-sync')

console.log(application)

StimulusReflex.initialize(application, { consumer })

import Document_Viewer from './controllers/document_viewer_controller'
import Subscription from './controllers/subscription_controller'
import Hotkeys from 'stimulus-hotkeys';

application.register("document_viewer", Document_Viewer)
application.register("subscription", Subscription)
application.register("hotkeys", Hotkeys)
