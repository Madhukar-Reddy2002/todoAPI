from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob
from pydantic import BaseModel
#import uvicorn

app = FastAPI(title="Sentiment Analysis API")

# Enable CORS (Cross-Origin Resource Sharing) to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    text: str

@app.post("/sentiment-analysis")
def sentiment_analysis(request: SentimentRequest):
    text = request.text
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0:
        sentiment = "positive"
    elif polarity < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "text": text,
        "sentiment": sentiment,
        "polarity": polarity,
        "subjectivity": subjectivity
    }

#if __name__ == '__main__':
    #uvicorn.run('app:app', port=8000)
