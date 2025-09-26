# Python Standard Library Only - Zero Dependencies
FROM python:3.9-slim

WORKDIR /app

# No external dependencies needed
COPY requirements-none.txt requirements.txt
RUN echo "No pip packages to install"

# Copy standard library application
COPY main_stdlib.py main.py

# Pure Python execution
CMD ["python", "main.py"]