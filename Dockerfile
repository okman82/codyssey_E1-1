FROM nginx:alpine
LABEL org.opencontainers.image.title="mani-workstation-web"
ENV APP_ENV=dev
COPY site/ /usr/share/nginx/html/
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q --spider http://127.0.0.1/ || exit 1
