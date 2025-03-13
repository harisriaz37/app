# Use a lightweight Python image
FROM python:3.10-slim  

# Set the working directory inside the container
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install dependencies without cache to save space
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for FastAPI
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
