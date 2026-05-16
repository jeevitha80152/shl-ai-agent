from fastapi import FastAPI
from models import ChatRequest, ChatResponse
from agent import get_recommendations

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = get_recommendations(
        messages=request.messages,
        user_name=request.user_name
    )

    return ChatResponse(
        reply=result["reply"],
        recommendations=result["recommendations"],
        end_of_conversation=result["end_of_conversation"]
    )