from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob
from pydantic import BaseModel
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import uvicorn

app = FastAPI(title="Text Analysis and Summarization API")

# Enable CORS (Cross-Origin Resource Sharing) to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentAnalysisRequest(BaseModel):
    text: str

class SummarizationRequest(BaseModel):
    text: str
    num_lines: int = 3  # Default to 3 lines in summary

@app.post("/sentiment-analysis")
def sentiment_analysis(request: SentimentAnalysisRequest):
    text = request.text

    # Sentiment Analysis
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0:
        sentiment = "positive"
    elif polarity < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    # Return sentiment analysis results
    return {
        "original_text": text,
        "sentiment_analysis": {
            "sentiment": sentiment,
            "polarity": polarity,
            "subjectivity": subjectivity
        }
    }

@app.post("/text-summarization")
def text_summarization(request: SummarizationRequest):
    text = request.text
    num_lines = request.num_lines

    # Summarization
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_lines)

    # Convert summary sentences back to a string
    summary_text = " ".join(str(sentence) for sentence in summary)

    # Return summarization results
    return {
        "original_text": text,
        "summarization": {
            "num_lines": num_lines,
            "summary": summary_text
        }
    }

#if __name__ == '__main__':
    #uvicorn.run('app:app', port=8000)
