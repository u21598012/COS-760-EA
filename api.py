from enum import IntEnum
from fastapi import FastAPI, HTTPException
import uvicorn
import os
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from lime.lime_text import LimeTextExplainer
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer
)
from peft import PeftModel
from fastapi.concurrency import run_in_threadpool

from MultiLabelClassifier import MultiLabelEmotionModel
from LimeExplainer import LimeMultiLabelEmotionExplainer

english_pretrained_model_path_xlm = 'KhweziSandi/XLM-R-Zero-Shot-Hausa'
hausa_finetuned_model_path_xlm = 'KhweziSandi/XLM-R-Fine-Tuned-Hausa'
hausa_finetuned_model_path_bert = 'rdhinaz/BERT-Fine-Tuned-Hausa'
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
   BERT_FT = 1  # BERT Fine-tuned model classification
   XLM_ZS = 2 # XLM-R Zero shot classification
   XLM_FT = 3 # XLM-R Fine-tuned model classification

def classifyText(text: str, model_type: ModelType, num_samples: int, threshold: float):
    explainer = models.get(model_type)
    if explainer is None:
        raise HTTPException(status_code=500, detail=f"Model '{model_type}' not loaded")

    return explainer.explain_instance(text, top_labels=6, num_samples=num_samples, decision_boundary=threshold)

@app.on_event("startup")
def load_models():
    global models
    print("Loading models...")

    model_configs = {
        ModelType.BERT_FT: hausa_finetuned_model_path_bert,
        ModelType.XLM_ZS: english_pretrained_model_path_xlm,
        ModelType.XLM_FT: hausa_finetuned_model_path_xlm,
    }

    for model_type, path in model_configs.items():
        
        print(f"Loading {model_type.name} model from {path}")
        tokenizer = AutoTokenizer.from_pretrained(path)

        if model_type in (ModelType.XLM_FT, ModelType.XLM_ZS):
            base_model = MultiLabelEmotionModel(MODEL_NAME, len(emotion_columns))
            model = PeftModel.from_pretrained(base_model, path)
        else:
            model = AutoModelForSequenceClassification.from_pretrained(path)


        explainer = LimeMultiLabelEmotionExplainer(model, tokenizer, emotion_columns)
        models[model_type] = explainer

    print("Model loading complete.")

# Type of model used for classification (from 0-3)
class Item(BaseModel):
    text: str = Field(..., example="Such an example text must be analyzed immediately!")
    model_type: ModelType = Field(..., example=3)
    lime_iterations: int = Field(..., example=1000)
    decision_boundary: float = Field(..., example=0.5)

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
   return await run_in_threadpool(classifyText, data.text, data.model_type, data.lime_iterations, data.decision_boundary)

if __name__ == "__main__":
   uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)