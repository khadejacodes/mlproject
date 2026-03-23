# 1. Use a standard Python image
FROM python:3.10-slim

# 2. Set the working directory
WORKDIR /app

# 3. Copy everything into the container
COPY . /app

# 4. Install your Python libraries
# (We skip apt-get update to avoid the Error 100)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expose the port
EXPOSE 8080

# 6. Start the app
CMD ["python", "app.py"]