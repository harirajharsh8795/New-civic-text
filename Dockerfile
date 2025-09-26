# BULLETPROOF - Python Standard Library Only
FROM python:3.9-slim

WORKDIR /app

# Copy application (uses only Python standard library)
COPY main_bulletproof.py main.py

# Run the application - Railway will provide PORT
CMD ["python", "main.py"]