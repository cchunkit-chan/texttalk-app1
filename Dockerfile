
# Use a basic Python 3.8 image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Download the SpaCy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application code
COPY . .

# Set the command to run the app
CMD ["streamlit", "run", "texttalk_app.py"]
