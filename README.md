# Tudlo Essay Summarizer with RAG + VectorDB (Setup for tudlo-server)

AI-powered essay summarization service using FastAPI, LlamaIndex, and Groq.

## 🚀 Setup Guide

### Prerequisites
- Python 3.11+ (recommended)
- Groq API key ([Get it here](https://console.groq.com/keys))

### 1. Go to backend directory
```bash
    cd tudlo-server
```

### 2. Setup Virtual Environment
```bash
    python3 -m venv .venv
```
```bash
    source .venv/bin/activate
```

### 3. Setup .env file (See .env.example for format)

### 4. Install Dependencies
```bash
    pip install -r requirements.txt
```

### 5. Run the Application
```bash
    uvicorn main:app --reload
```

## Troubleshooting
### Missing python.h
```bash
  sudo apt install python3-dev
```

### Cannot install chromadb
```bash
  sudo apt install -y python3.13-dev build-essential cmake g++
```





# Setup for tudlo-client

## Setting up

Go to the frontend directory

```bash
    cd tudlo-client
```

Install dependencied with
```bash
    pnpm install
```

You may  change 'pnpm' depending on your package installer.


## Building

To create a production version of your app:

```bash
    pnpm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://svelte.dev/docs/kit/adapters) for your target environment.
## Drizzle
- You will need to set `DATABASE_URL` in your production environment.
- Run 
```bash
  pnpm run db:start
```
to start the Docker container.
- Run 
```bash
  pnpm run db:push
``` 
to update your database schema.