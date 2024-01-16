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
        class SummarizeRequest(BaseModel):
    text: str
    num_lines: int = 3  # Default to 5 lines in summary

@app.post("/summarize")
def summarize(request: SummarizeRequest):
    text = request.text
    num_lines = request.num_lines

    # Use Sumy library for summarization
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_lines)

    # Convert summary sentences back to a string
    summary_text = " ".join(str(sentence) for sentence in summary)

    return {
        "original_text": text,
        "summary": summary_text
    }

#if __name__ == '__main__':
    #uvicorn.run('app:app', port=8000)
