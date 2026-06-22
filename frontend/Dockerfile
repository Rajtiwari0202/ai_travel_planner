FROM node:22-slim

WORKDIR /app
COPY frontend/package*.json /app/
RUN npm ci \
    && chown -R node:node /app
COPY --chown=node:node frontend /app
USER node

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
