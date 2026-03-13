# Build stage
FROM node:20-slim as build

WORKDIR /app

# Install dependencies first for better caching
COPY package*.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port Vite runs on in dev mode
EXPOSE 5173

# Command to run Vite in dev mode with host exposed
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
