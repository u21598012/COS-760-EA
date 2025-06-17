from torch import nn
from transformers import (
    AutoModel,
    AutoConfig,  
)

class MultiLabelEmotionModel(nn.Module):
    """Multilabel emotion classification model based on paraphrase-xlm-r-multilingual-v1"""

    def __init__(self, model_name: str, num_labels: int, dropout_rate: float = 0.3):
        super().__init__()
        self.config = AutoConfig.from_pretrained(model_name)
        self.backbone = AutoModel.from_pretrained(model_name)
        self.num_labels = num_labels

        # Add classification head for multilabel prediction
        self.dropout = nn.Dropout(dropout_rate)
        self.classifier = nn.Linear(self.config.hidden_size, num_labels)

    def forward(self, input_ids, attention_mask=None, labels=None, **kwargs):
        outputs = self.backbone(input_ids=input_ids, attention_mask=attention_mask)

        # Use [CLS] token representation
        pooled_output = outputs.last_hidden_state[:, 0, :]  # [CLS] token
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)

        loss = None
        if labels is not None:
            # Use BCEWithLogitsLoss for multilabel classification
            loss_fn = nn.BCEWithLogitsLoss()
            loss = loss_fn(logits, labels.float())

        return {"loss": loss, "logits": logits}