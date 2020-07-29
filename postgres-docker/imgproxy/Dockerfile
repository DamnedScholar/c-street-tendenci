FROM darthsim/imgproxy:latest

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
  && apk --no-cache upgrade \
  && apk add --no-cache nginx

RUN echo -e "#!/bin/bash\nnginx && imgproxy" > /usr/local/bin/imgproxy-nginx
RUN chmod +x /usr/local/bin/imgproxy-nginx
RUN mkdir -p /run/nginx

ADD default.conf default.conf
ADD cert.pem /etc/letsencrypt/live/eclectic-co.com/fullchain.pem
ADD key.pem /etc/letsencrypt/live/eclectic-co.com/privkey.pem

CMD ["/usr/local/bin/imgproxy-nginx"]
