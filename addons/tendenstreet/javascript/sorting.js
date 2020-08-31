import { Application } from 'stimulus'
// import StimulusReflex from 'stimulus_reflex'
// import WebsocketConsumer from 'sockpuppet-js'
import SortingController from './controllers/sorting_controller'


const application = Application.start()
// const consumer = new WebsocketConsumer('ws://localhost:8000/ws/sockpuppet-sync')

application.register("sorting", SortingController)
// StimulusReflex.initialize(application, { consumer })
