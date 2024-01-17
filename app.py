from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob
from pydantic import BaseModel
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
#import uvicorn

app = FastAPI(title="Text Analysis and Summarization API")

# Enable CORS (Cross-Origin Resource Sharing) to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeAndSummarizeRequest(BaseModel):
    text: str
    num_lines: int = 3  # Default to 3 lines in summary

@app.post("/analyze-and-summarize")
def analyze_and_summarize(request: AnalyzeAndSummarizeRequest):
    text = request.text
    num_lines = request.num_lines

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

    # Summarization
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_lines)

    # Convert summary sentences back to a string
    summary_text = " ".join(str(sentence) for sentence in summary)

    # Return combined results
    return {
        "original_text": text,
        "sentiment_analysis": {
            "sentiment": sentiment,
            "polarity": polarity,
            "subjectivity": subjectivity
        },
        "summarization": {
            "num_lines": num_lines,
            "summary": summary_text
        }
    }

#if __name__ == '__main__':
    #uvicorn.run('app:app', port=8000)
