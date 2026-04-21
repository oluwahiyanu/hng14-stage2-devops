FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev

FROM node:20-slim
RUN apk update && apk upgrade && rm -rf /var/cache/apk/*
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
RUN useradd -m -u 1001 appuser
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"
CMD ["node", "app.js"]
