import { Application } from 'stimulus'
import StimulusReflex from 'stimulus_reflex'
import WebsocketConsumer from 'sockpuppet-js'
import Reactive_DirectoryController from './controllers/reactive_directory_controller'

const application = Application.start()
const consumer = new WebsocketConsumer('ws://localhost:8000/ws/sockpuppet-sync')

application.register("reactive_directory", Reactive_DirectoryController)
StimulusReflex.initialize(application, { consumer })
