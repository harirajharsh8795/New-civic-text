# BULLETPROOF - Python Standard Library Only
FROM python:3.9-slim

WORKDIR /app

# Copy Railway-optimized application
COPY main_railway_optimized.py main.py

# Run the application - Railway will provide PORT
CMD ["python", "main.py"]