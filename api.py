from enum import IntEnum
from fastapi import FastAPI, HTTPException
import uvicorn
import os
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from lime.lime_text import LimeTextExplainer
from transformers import (
    AutoTokenizer
)
from peft import PeftModel
from fastapi.concurrency import run_in_threadpool

from MultiLabelClassifier import MultiLabelEmotionModel
from LimeExplainer import LimeMultiLabelEmotionExplainer

english_pretrained_model_path = './models/zero_shot'
hausa_finetuned_model_path = './models/fine_tuned_hausa'
emotion_columns = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise']
MODEL_NAME = "sentence-transformers/paraphrase-xlm-r-multilingual-v1"
# MAX_LENGTH = 128

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global models dict
models = {}

class ModelType(IntEnum):
   XLM_ZS = 2 # Zero shot classification
   XLM_FT = 3 # Fine tuned model classification

def classifyText(text: str, model_type: ModelType):
    explainer = models.get(model_type)
    if explainer is None:
        raise HTTPException(status_code=500, detail=f"Model '{model_type}' not loaded")

    return explainer.explain_instance(text, top_labels=6, num_samples=1000)

@app.on_event("startup")
def load_models():
    global models
    print("Loading models...")

    model_configs = {
        ModelType.XLM_ZS: english_pretrained_model_path,
        ModelType.XLM_FT: hausa_finetuned_model_path,
    }

    for model_type, path in model_configs.items():
        if not os.path.exists(path):
            print(f"Warning: Model path does not exist - {path}")
            continue

        print(f"Loading {model_type.name} model from {path}")
        tokenizer = AutoTokenizer.from_pretrained(path)
        base_model = MultiLabelEmotionModel(MODEL_NAME, len(emotion_columns))
        model = PeftModel.from_pretrained(base_model, path)
        explainer = LimeMultiLabelEmotionExplainer(model, tokenizer, emotion_columns)
        models[model_type] = explainer

    print("Model loading complete.")

# Type of model used for classification (from 0-3)
class Item(BaseModel):
    text: str = Field(..., example="Such an example text must be analyzed immediately!")
    model_type: ModelType = Field(..., example=3)

    class Config:
        schema_extra = {
            "example": {
                "text": "Such an example text must be analyzed immediately!",
                "model_type": 3
            }
        }

@app.get("/")
async def root():
   return {"message": "Hello World"}

@app.post("/")
async def analyseText(data: Item):
   return await run_in_threadpool(classifyText, data.text, data.model_type)

if __name__ == "__main__":
   uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)