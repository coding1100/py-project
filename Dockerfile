# Use a Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the necessary files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Define environment variables (you should not hard-code sensitive data)
ENV OPENAI_ENDPOINT="https://thirdwishgroup-ai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"
ENV API_KEY="e78c273f6f844dd2bb0f00fdba023b6a"

# Run the application
CMD ["python", "process_problems.py", "--num_rounds", "3", "--num_problems", "5", "--topk_problems", "3"]