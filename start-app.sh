#!/bin/bash

# Task Intelligence App - Quick Start Script for Codespaces

echo "=================================================="
echo "🚀 Starting Task Intelligence App"
echo "=================================================="

# Check if backend/.env exists
if [ ! -f backend/.env ]; then
    echo "⚠️  Warning: backend/.env not found"
    echo "Please configure your API keys first!"
    echo "See CODESPACES_SETUP.md for instructions"
    exit 1
fi

# Function to check if port is in use
check_port() {
    lsof -ti:$1 > /dev/null 2>&1
}

# Kill processes on ports if they exist
if check_port 8000; then
    echo "Stopping existing backend on port 8000..."
    lsof -ti:8000 | xargs kill -9
fi

if check_port 5173; then
    echo "Stopping existing frontend on port 5173..."
    lsof -ti:5173 | xargs kill -9
fi

echo ""
echo "Starting Backend API..."
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

sleep 3

echo "Starting Frontend..."
cd frontend
npm run dev -- --host > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "=================================================="
echo "✅ Services Started!"
echo "=================================================="
echo ""
echo "Backend API (PID: $BACKEND_PID)"
echo "  - Running on port 8000"
echo "  - API Docs: Check PORTS tab for URL + /docs"
echo "  - Logs: tail -f /tmp/backend.log"
echo ""
echo "Frontend (PID: $FRONTEND_PID)"
echo "  - Running on port 5173"
echo "  - Access: Check PORTS tab in VS Code"
echo "  - Logs: tail -f /tmp/frontend.log"
echo ""
echo "To stop services:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "=================================================="
