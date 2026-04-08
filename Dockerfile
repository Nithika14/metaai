FROM python:3.11-slim

WORKDIR /app

COPY . /app

# Install required dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# By default, trigger the evaluation script
CMD ["python", "inference.py"]
