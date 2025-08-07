#!/bin/bash

# Start Ollama in the background
ollama serve &

# Wait for Ollama to start (you can fine-tune the delay)
sleep 10

# Pull the model you need (Gemma 2B - smaller size)
ollama pull gemma2:2b

# Keep container running
wait
