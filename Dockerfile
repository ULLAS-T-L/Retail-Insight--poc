FROM python:3.10-slim

# Set strict unprivileged active variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

# Initialize workspace bounds
WORKDIR /app

# Safely copy dependency bindings
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Migrate logic vectors securely
COPY . .

# Launch service dynamically locally efficiently
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
