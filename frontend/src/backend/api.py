from enum import IntEnum
from fastapi import FastAPI, HTTPException
import uvicorn
import os
# from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
# from lime.lime_text import LimeTextExplainer
# from transformers import (
#     AutoTokenizer
# )
# from peft import PeftModel
from fastapi.concurrency import run_in_threadpool

# from MultiLabelClassifier import MultiLabelEmotionModel
# from LimeExplainer import LimeMultiLabelEmotionExplainer

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

# class ModelType(IntEnum):
#    XLM_ZS = 2 # Zero shot classification
#    XLM_FT = 3 # Fine tuned model classification

# def classifyText(text: str, model_type: ModelType):
#     explainer = models.get(model_type)
#     if explainer is None:
#         raise HTTPException(status_code=500, detail=f"Model '{model_type}' not loaded")

#     return explainer.explain_instance(text, top_labels=6, num_samples=1000)

# @app.on_event("startup")
# def load_models():
#     global models
#     print("Loading models...")

#     model_configs = {
#         ModelType.XLM_ZS: english_pretrained_model_path,
#         ModelType.XLM_FT: hausa_finetuned_model_path,
#     }

#     for model_type, path in model_configs.items():
#         if not os.path.exists(path):
#             print(f"Warning: Model path does not exist - {path}")
#             continue

#         print(f"Loading {model_type.name} model from {path}")
#         tokenizer = AutoTokenizer.from_pretrained(path)
#         base_model = MultiLabelEmotionModel(MODEL_NAME, len(emotion_columns))
#         model = PeftModel.from_pretrained(base_model, path)
#         explainer = LimeMultiLabelEmotionExplainer(model, tokenizer, emotion_columns)
#         models[model_type] = explainer

#     print("Model loading complete.")

# # Type of model used for classification (from 0-3)
# class Item(BaseModel):
#     text: str = Field(..., example="Such an example text must be analyzed immediately!")
#     model_type: ModelType = Field(..., example=3)

#     class Config:
#         schema_extra = {
#             "example": {
#                 "text": "Such an example text must be analyzed immediately!",
#                 "model_type": 3
#             }
#         }

@app.get("/")
async def root():
   return {
    "text": "Such an example text must be analyzed immediately!",
    "predictions": {
        "anger": 0.05183861404657364,
        "disgust": 0.0014993679942563176,
        "fear": 0.17420588433742523,
        "joy": 0.6161146759986877,
        "sadness": 0.004311972297728062,
        "surprise": 0.9096109867095947
    },
    "explanations": {
        "surprise": [
            [
                "immediately",
                0.1645227275223517
            ],
            [
                "Such",
                0.08372206955786717
            ],
            [
                "an",
                0.069272314646481
            ],
            [
                "analyzed",
                -0.059914105064036736
            ],
            [
                "be",
                0.019068045874210928
            ],
            [
                "text",
                -0.007481882380973626
            ],
            [
                "example",
                -0.006287201931452925
            ],
            [
                "must",
                -0.0005878872959629906
            ]
        ],
        "joy": [
            [
                "example",
                0.2891770693965019
            ],
            [
                "must",
                -0.1622107808891679
            ],
            [
                "be",
                -0.05145106547586627
            ],
            [
                "Such",
                -0.03021134275942115
            ],
            [
                "an",
                0.023857096360395603
            ],
            [
                "immediately",
                0.019801818806735146
            ],
            [
                "analyzed",
                0.01412757882404612
            ],
            [
                "text",
                0.008957726249979198
            ]
        ],
        "fear": [
            [
                "example",
                -0.1959927371783523
            ],
            [
                "immediately",
                0.11053350347068275
            ],
            [
                "must",
                0.07801305803376282
            ],
            [
                "analyzed",
                -0.052549456854236905
            ],
            [
                "be",
                0.04411625356237659
            ],
            [
                "text",
                -0.032649120117486066
            ],
            [
                "Such",
                0.021940065159383768
            ],
            [
                "an",
                -0.0003197554961544433
            ]
        ],
        "anger": [
            [
                "immediately",
                0.021968042468139305
            ],
            [
                "example",
                -0.010787941855067385
            ],
            [
                "an",
                -0.01052595550391198
            ],
            [
                "must",
                -0.008586178938456616
            ],
            [
                "be",
                -0.006473962726486519
            ],
            [
                "Such",
                -0.006170211795835053
            ],
            [
                "analyzed",
                0.0033978207651435216
            ],
            [
                "text",
                0.0011690974791734672
            ]
        ],
        "sadness": [
            [
                "immediately",
                -0.004689994787665476
            ],
            [
                "text",
                -0.0023162019354309965
            ],
            [
                "analyzed",
                -0.0022038405393659116
            ],
            [
                "an",
                -0.0013477214549451355
            ],
            [
                "must",
                -0.0011711493903291117
            ],
            [
                "example",
                -0.0006366586501568469
            ],
            [
                "Such",
                0.0003576276254710991
            ],
            [
                "be",
                1.6335786655888513e-05
            ]
        ],
        "disgust": [
            [
                "must",
                -0.001527061738309549
            ],
            [
                "example",
                0.0008676382156153018
            ],
            [
                "text",
                -0.0006582400123729504
            ],
            [
                "be",
                -0.00043405350311871845
            ],
            [
                "analyzed",
                -0.00035297695667133234
            ],
            [
                "immediately",
                0.0001536846183568011
            ],
            [
                "Such",
                -7.920107936648744e-05
            ],
            [
                "an",
                1.532821292694793e-05
            ]
        ]
    }
}

# @app.post("/")
# async def analyseText(data: Item):
#    return await run_in_threadpool(classifyText, data.text, data.model_type)

if __name__ == "__main__":
   uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)