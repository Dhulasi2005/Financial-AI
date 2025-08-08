from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import logging

# Initialize once and reuse
_sentiment_pipeline = None

def get_sentiment_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        # model name used widely for financial tone classification
        model_name = "yiyanghkust/finbert-tone"
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(model_name)
            _sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
        except Exception as e:
            logging.error("Unable to load FinBERT model: %s", e)
            raise
    return _sentiment_pipeline

def analyze_text(text):
    """
    Returns (label, score) where label is 'positive'|'neutral'|'negative' and score is confidence.
    """
    pipe = get_sentiment_pipeline()
    out = pipe(text[:512])  # limit length
    # output example: [{'label': 'neutral', 'score': 0.83}]
    if len(out) > 0:
        label = out[0]['label'].lower()
        score = float(out[0]['score'])
        return label, score
    return "neutral", 0.0