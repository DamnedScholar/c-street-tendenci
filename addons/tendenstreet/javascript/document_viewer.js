import { Application } from 'stimulus'
// import StimulusReflex from 'stimulus_reflex'
// import WebsocketConsumer from 'sockpuppet-js'
import Document_ViewerController from './controllers/document_viewer_controller'

const application = Application.start()
// const consumer = new WebsocketConsumer('ws://localhost:8000/ws/sockpuppet-sync')

application.register("document_viewer", Document_ViewerController)
// StimulusReflex.initialize(application, { consumer })
