import { Application } from 'stimulus'
// import StimulusReflex from 'stimulus_reflex'
// import WebsocketConsumer from 'sockpuppet-js'
import Document_Viewer from './controllers/document_viewer_controller'
import Hotkeys from 'stimulus-hotkeys';

const application = Application.start()
// const consumer = new WebsocketConsumer('ws://localhost:8000/ws/sockpuppet-sync')

application.register("document_viewer", Document_Viewer)
application.register("hotkeys", Hotkeys)
// StimulusReflex.initialize(application, { consumer })
