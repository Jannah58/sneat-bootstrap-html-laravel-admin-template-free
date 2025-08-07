# Ollama FastAPI Chat Interface with Gemma 2B

A modern web interface for interacting with Ollama models through FastAPI, now using the lightweight Gemma 2B model with LangChain integration.

## Features

✅ **Modern Chat UI**: Beautiful, responsive design with chat bubbles
🔄 **Model Status Indicator**: Shows when the model is loading, ready, or has errors
📤 **Easy Input**: Text area with auto-resize and Enter-to-send
💬 **Real-time Responses**: Displays loading states during generation
🎨 **Mobile Friendly**: Responsive design that works on all devices
🤖 **Gemma 2B Model**: Lightweight Google Gemma 2B model for efficient performance
🔗 **LangChain Integration**: Enhanced prompt handling and response processing

## Quick Start

1. **Start the services**:
   ```bash
   docker-compose up
   ```

2. **Open your browser** and go to:
   ```
   http://localhost:8000
   ```
   also make sure that the model is available by seeing ✅ Ready (gemma2:2b) at the web page if Not Run 
   ```
   docker exec -it ollama ollama pull gemma:2b
  ```
  And Then 
  ```
  docker exec -it ollama ollama list
  ```
  This way you ensure everything is ready :)

3. **Wait for the model to load** - you'll see:
   - 🔄 "Loading model..." initially
   - ✅ "Ready" when the model is available
   - ❌ Error message if something goes wrong  

4. **Start chatting**! Type your message and press Enter or click the 📤 button.

## How it Works

### Backend (FastAPI)
- **`/`** - Serves the HTML frontend
- **`/status`** - Returns model availability status
- **`/generate`** - Processes chat messages and returns AI responses (direct API)
- **`/chat`** - New LangChain-powered endpoint with enhanced prompt processing
- **`/static`** - Serves static files (HTML, CSS, JS)

### Frontend (HTML + JavaScript)
- **Model Status Checking**: Automatically checks if Ollama is ready
- **Disabled State**: Input is disabled until model is ready
- **Loading Indicators**: Shows spinners during processing
- **Error Handling**: Displays user-friendly error messages
- **Auto-scroll**: Chat area automatically scrolls to latest messages

## API Endpoints

### Check Model Status
```http
GET /status
```
Response:
```json
{
  "status": "ready|loading|error",
  "model": "gemma2:2b",
  "message": "Optional status message"
}
```

### Generate Response (Direct API)
```http
POST /generate
Content-Type: application/json

{
  "prompt": "Your message here"
}
```
Response:
```json
{
  "response": "AI generated response"
}
```

### Chat with LangChain 
```http
POST /chat
Content-Type: application/json

{
  "message": "Your message here",
  "use_langchain": true
}
```
Response:
```json
{
  "response": "AI generated response",
  "model": "gemma2:2b",
  "method": "langchain"
}
```

## Development

The frontend is a single HTML file with embedded CSS and JavaScript for simplicity. All the interactive features are handled client-side:

- **Real-time status updates** every 5 seconds
- **Input validation** and state management
- **Responsive design** with modern CSS gradients
- **Smooth animations** and transitions

## Troubleshooting

- **"Loading model..." persists**: Check if Ollama service is running
- **"No model found"**: Ensure Gemma 2B model is pulled in Ollama
- **Connection errors**: Verify docker-compose networking
- **LangChain errors**: Check that langchain dependencies are installed

## Model Information

**Gemma 2B** is a lightweight language model from Google that provides:
- **Smaller size**: Significantly smaller than Llama 2, saving disk space and memory
- **Faster inference**: Quicker response times due to smaller model size
- **Good performance**: Maintains good quality for most conversational tasks
- **Lower resource requirements**: Better suited for systems with limited resources

Enjoy chatting with your AI model! 🤖