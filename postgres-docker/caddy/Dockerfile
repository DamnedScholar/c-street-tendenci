FROM caddy:2-builder-alpine AS builder

RUN xcaddy build \
    --with https://github.com/abiosoft/caddy-exec \
    --with https://github.com/caddyserver/nginx-adapter \
    --with https://github.com/greenpau/caddy-auth-portal \
    --with https://github.com/greenpau/caddy-auth-jwt \
    --with https://github.com/greenpau/caddy-trace \
    --with https://github.com/hairyhenderson/caddy-teapot-module \
    --with https://github.com/lucaslorentz/caddy-docker-proxy

FROM caddy:2.2.1

COPY --from=builder /usr/bin/caddy /usr/bin/caddy
