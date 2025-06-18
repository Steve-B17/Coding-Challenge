import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Debug prints
print("Current working directory:", os.getcwd())
print("Environment variables loaded:", os.environ.get("GROQ_KEY", "Not found"))

from src.app import app

@app.get("/")
def read_root():
    return {"message": "Backend is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)