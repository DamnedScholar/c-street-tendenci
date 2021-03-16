import { Controller } from "stimulus"
import { init } from '@sentry/browser';

export default class extends Controller {

  connect() {
    init({ dsn: 'https://b8f314147659498982aba093ae14be48@o552263.ingest.sentry.io/5677642' });
  }
}
