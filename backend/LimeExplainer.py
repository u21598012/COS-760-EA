from lime.lime_text import LimeTextExplainer
import numpy as np
import matplotlib.pyplot as plt
import torch
from typing import List, Dict, Tuple

class LimeMultiLabelEmotionExplainer:
    """
    LIME explainer wrapper for multilabel emotion classification models
    """

    def __init__(self, model, tokenizer, emotion_columns: List[str], device='cuda' if torch.cuda.is_available() else 'cpu'):

        self.model = model
        self.tokenizer = tokenizer
        self.emotion_columns = emotion_columns
        self.device = device
        self.model.to(device)
        self.model.eval()

        self.explainer = LimeTextExplainer(
            class_names=emotion_columns
        )

    def predict_proba(self, texts: List[str]) -> np.ndarray:
        """
        Args:
            texts: List of text strings to predict

        Returns:
            numpy array of shape (n_samples, n_emotions) with probabilities
        """
        self.model.eval()
        predictions = []

        with torch.no_grad():
            for text in texts:
                # Tokenize the text
                inputs = self.tokenizer(
                    text,
                    return_tensors='pt',
                    truncation=True,
                    padding=True,
                    max_length=512
                ).to(self.device)

                # Get model predictions
                outputs = self.model(**inputs)
                logits = outputs['logits']

                # Convert to probabilities using sigmoid (for multilabel)
                probs = torch.sigmoid(logits).cpu().numpy().flatten()
                predictions.append(probs)

        return np.array(predictions)

    def explain_instance(self, text: str, decision_boundary: float = 0.5, top_labels: int = None, num_features: int = 10,
                        num_samples: int = 400) -> Dict:
        """
        Args:
            text: Text to explain
            top_labels: Number of top emotions to explain (None for all)
            num_features: Number of words to include in explanation
            num_samples: Number of samples for LIME

        Returns:
            Dictionary containing explanations and predictions
        """
        # Get prediction for the original text
        original_pred = self.predict_proba([text])[0]
        predicted_labels = (original_pred >= decision_boundary).astype(int)

        # Determine which emotions to explain
        if top_labels is None:
            labels_to_explain = list(range(len(self.emotion_columns)))
        else:
            # Get top `top_labels` predicted emotions
            top_indices = np.argsort(original_pred)[-top_labels:][::-1]
            labels_to_explain = top_indices.tolist()

        # Generate LIME explanation
        explanation = self.explainer.explain_instance(
            text,
            self.predict_proba,
            labels=labels_to_explain,
            num_features=num_features,
            num_samples=num_samples
        )


        results = {
            'text': text,
            'probabilities': {emotion: float(prob) for emotion, prob in zip(self.emotion_columns, original_pred)},
            'predictions': {emotion: bool(pred) for emotion, pred in zip(self.emotion_columns, predicted_labels)},
            'explanations': {}
        }

        # Extract explanations for each emotion
        for label_idx in labels_to_explain:
            emotion_name = self.emotion_columns[label_idx]
            word_importance = explanation.as_list(label=label_idx)
            results['explanations'][emotion_name] = word_importance

        return results

    def visualize_explanation(self, explanation_result: Dict, emotion: str = None,
                            save_path: str = None, figsize: Tuple[int, int] = (12, 8)):

        explanations = explanation_result['explanations']
        predictions = explanation_result['predictions']

        if emotion and emotion in explanations:
            emotions_to_plot = [emotion]
        else:
            emotions_to_plot = list(explanations.keys())

        n_emotions = len(emotions_to_plot)
        fig, axes = plt.subplots(n_emotions, 1, figsize=figsize, squeeze=False)

        for i, emotion_name in enumerate(emotions_to_plot):
            ax = axes[i, 0]
            word_importance = explanations[emotion_name]

            # Separate positive and negative influences
            words = [item[0] for item in word_importance]
            scores = [item[1] for item in word_importance]

            # Create color map based on positive/negative influence
            colors = ['green' if score > 0 else 'red' for score in scores]

            # Create horizontal bar plot
            y_pos = np.arange(len(words))
            bars = ax.barh(y_pos, scores, color=colors, alpha=0.7)

            ax.set_yticks(y_pos)
            ax.set_yticklabels(words)
            ax.set_xlabel('Importance Score')
            ax.set_title(f'{emotion_name} (Prediction: {predictions[emotion_name]:.3f})')
            ax.grid(axis='x', alpha=0.3)

            # Add vertical line at x=0
            ax.axvline(x=0, color='black', linestyle='-', alpha=0.3)

        plt.tight_layout()
        plt.suptitle(f'LIME Explanations\nText: "{explanation_result["text"][:100]}..."',
                     y=1.02, fontsize=12)

        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)

        plt.show()