
echo "==================================================="
echo "  KINETIX - Autonomous Local Text-to-Video Studio"
echo "  Developed by JOJIN JOHN"
echo "==================================================="
echo.

cd /d "%~dp0"

echo "[1/3] Starting Kinetix Backend on http://127.0.0.1:8000 ..."

cd backend 
source venv\Scripts\activate.bat 
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload



echo "[2/3] Starting Kinetix Frontend on http://localhost:3000 ..."
echo "Kinetix Frontend Studio"  
cd frontend && npm run dev"



echo "[3/3] Opening Kinetix Studio in your default browser..."
open http://localhost:3000

echo "."
echo "==================================================="
echo "  Kinetix is running!"
echo "  Studio UI: http://localhost:3000"
echo "  API Docs:  http://127.0.0.1:8000/docs"
echo "==================================================="

