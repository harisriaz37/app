# Use a smaller Alpine-based Python image
FROM python:3.10-alpine  

# Set working directory
WORKDIR /app  

# Install dependencies (optimize to avoid extra layers)
RUN apk add --no-cache gcc musl-dev libc-dev \
    && pip install --no-cache-dir --upgrade pip setuptools wheel 

# Copy only necessary files
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the rest of the app
COPY . /app  

# Expose the FastAPI port
EXPOSE 8000  

# Run FastAPI with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
