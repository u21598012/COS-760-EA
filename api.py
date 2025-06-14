from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from lime.lime_text import LimeTextExplainer

app = FastAPI()

@app.get("/")
async def root():
   return {"message": "Hello World"}

if __name__ == "__main__":
   uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)