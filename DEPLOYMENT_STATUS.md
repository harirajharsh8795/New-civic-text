# Railway Deployment Guide

## Current Status: FIXING HEALTHCHECK FAILURE

The issue is Railway keeps failing healthcheck even though build succeeds.

## Method 1: FastAPI (Current)
- Uses `main.py` with FastAPI + uvicorn
- Dependencies: fastapi, uvicorn, pydantic
- Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Method 2: Backup (Zero Dependencies)
If FastAPI keeps failing, switch to backup:

1. Rename files:
   ```bash
   mv main.py main_fastapi.py
   mv backup_server.py main.py
   mv requirements.txt requirements-fastapi.txt
   mv requirements-backup.txt requirements.txt
   ```

2. Update Procfile:
   ```
   web: python main.py
   ```

3. Push changes

## Current Railway Configuration:
- Builder: nixpacks (no Dockerfile)
- Start: uvicorn command from railway.json
- Health: /health endpoint
- Port: $PORT environment variable

## If Still Failing:
Try switching railway.json builder to "heroku" or remove railway.json entirely and let Railway auto-detect.