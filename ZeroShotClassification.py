import torch
import pandas as pd
from datasets import load_dataset

class ZeroShotPredictor():

    def __init__(self):
        print("Class initialized")

    def predict_emotions(self, text: str, model, tokenizer, emotion_columns, threshold=0.5, device='cpu'):
        """Zero-shot emotion prediction for Hausa text using multilingual model"""
        model.eval()
        model.to(device)

        # Tokenize Hausa input
        inputs = tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=512,
            return_tensors='pt'
        )

        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = torch.sigmoid(outputs['logits']).cpu().numpy()[0]

        # Convert to binary predictions
        predictions = probabilities > threshold

        results = []
        for i, (emotion, prob, pred) in enumerate(zip(emotion_columns, probabilities, predictions)):
            results.append({
                'emotion': emotion,
                'probability': prob,
                'predicted': bool(pred)
            })

        results.sort(key=lambda x: x['probability'], reverse=True)
        return results


    """Run zero-shot inference on Hausa data using an English-trained model"""
    def run_zero_shot_hausa_inference(self, model, tokenizer, emotion_columns, threshold=0.5, num_samples=10):
        print("\n=== Zero-Shot Inference on Hausa Subset ===")

        # Load Hausa test set
        dataset = load_dataset("brighter-dataset/BRIGHTER-emotion-categories", "hau")
        hausa_df = pd.DataFrame(dataset['test'])

        # Drop rows with empty text
        hausa_df = hausa_df.dropna(subset=['text'])

        # Pick a subset for prediction
        texts = hausa_df['text'].tolist()[:num_samples]

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        for i, text in enumerate(texts):
            print(f"\nSample {i + 1}: '{text}'")
            results = self.predict_emotions(text, model, tokenizer, emotion_columns, threshold, device)

            print("Predicted emotions:")
            for result in results:
                status = "✓" if result['predicted'] else " "
                print(f"  {status} {result['emotion']:>8}: {result['probability']:.3f}")

            predicted_emotions = [r['emotion'] for r in results if r['predicted']]
            print(f"Final prediction: {predicted_emotions if predicted_emotions else 'No emotions detected'}")
            print("-" * 60)
