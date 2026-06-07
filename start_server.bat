@echo off
cd /d D:\WorkSpace\Claude_Code\Latest_News_Tech
set PORT=8080
"D:\WorkSpace\Claude_Code\Latest_News_Tech\.venv\Scripts\python.exe" -m uvicorn main_v2:app --host 0.0.0.0 --port 8080 > "D:\WorkSpace\Claude_Code\Latest_News_Tech\server_rb.log" 2>&1
