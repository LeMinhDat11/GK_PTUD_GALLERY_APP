#!/bin/bash

echo "🚀 Starting Gallery App..."
echo ""

# Start backend
echo "📦 Starting FastAPI backend on http://localhost:8000"
cd "$(dirname "$0")/backend"
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

sleep 1

# Start frontend
echo "⚛️  Starting React frontend on http://localhost:3000"
cd "$(dirname "$0")/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ App running!"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"

wait $BACKEND_PID $FRONTEND_PID
