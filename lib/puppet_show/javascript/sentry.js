import * as Sentry from "@sentry/browser"
import { Integrations as TracingIntegrations } from "@sentry/tracing"

Sentry.init({
    dsn: 'https://b8f314147659498982aba093ae14be48@o552263.ingest.sentry.io/5677642',
    integrations: [new TracingIntegrations.BrowserTracing()],
})

export default Sentry
