FROM darthsim/imgproxy:latest

RUN apt update \
  && apt install -o APT::Get::Assume-Yes=true nginx

RUN export IMGPROXY_KEY=a780243df2e5c90dd05fbe0ff81b82fe6086f43cf7acd240a2ae76389bc630d419eca9e478c63b5aa6e9da11a1e0a9d7af9a0dc9e840f0e4291ba722ccb647db
RUN export IMGPROXY_SALT=89367b50dea8a1de807a25df11bdbc81107b54b10f564c617f0509a949e06402e8c842b47a7bfd51c1bd2ca6941b336b5776174edfe415c01cf80793d3b8de0b


RUN echo -e "#!/bin/bash/nginx && imgproxy" > /usr/local/bin/imgproxy-nginx
RUN chmod +x /usr/local/bin/imgproxy-nginx
RUN mkdir -p /run/nginx

ADD default.conf /etc/nginx/conf.d/default.conf
ADD cert.pem /etc/nginx/ssl/cert.pem
ADD key.pem /etc/nginx/ssl/key.pem

CMD ["/usr/local/bin/imgproxy-nginx"]
