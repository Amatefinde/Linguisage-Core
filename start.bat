@echo off
REM Запуск первого микросервиса
start cmd /k "cd E:/all/studying/Linguisage-Content && E:/all/studying/Linguisage-Content/venv/Scripts/activate && uvicorn main:app --reload --host 192.168.31.23 --port 4444"
REM Запуск второго микросервиса
start cmd /k "cd E:/all/studying/Linguisage-Authentification && venv/Scripts/activate && uvicorn main:app --reload --host 192.168.31.23 --port 8001"