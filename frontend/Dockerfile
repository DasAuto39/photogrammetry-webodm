FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
COPY entrypoint.sh /docker-entrypoint.d/99-envsubst.sh
RUN chmod +x /docker-entrypoint.d/99-envsubst.sh
CMD ["nginx", "-g", "daemon off;"]
