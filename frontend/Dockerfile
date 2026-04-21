FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev

FROM node:20-slim
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .

# --- UPDATED USER CREATION PATTERN ---
RUN addgroup --system appuser && adduser --system --ingroup appuser appuser
USER appuser
# -------------------------------------

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

CMD ["node", "app.js"]