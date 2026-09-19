from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from ollama import AsyncClient
from pydantic import BaseModel

app = FastAPI()
client = AsyncClient()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(request: ChatRequest):
    async def generate():
        async for chunk in await client.chat(
            model="llama3.2:3b",
            messages=[{"role": "user", "content": request.message}],
            stream=True,
        ):
            yield chunk["message"]["content"]

    return StreamingResponse(generate(), media_type="text/plain")