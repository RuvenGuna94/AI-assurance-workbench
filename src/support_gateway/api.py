import os
from pathlib import Path

import httpx
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Northstar Support Gateway",
    version="0.1.0",
)

SYSTEM_PROMPT = (
    Path(__file__)
    .with_name("system_prompt.txt")
    .read_text(encoding="utf-8")
)

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434/v1",
)
OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:3b-instruct-q4_K_M",
)
APP_API_KEY = os.getenv(
    "APP_API_KEY",
    "local-lab-key",
)
TIMEOUT = float(
    os.getenv("REQUEST_TIMEOUT_SECONDS", "120")
)


class Message(BaseModel):
    role: str
    content: str = Field(min_length=1, max_length=8000)


class ChatRequest(BaseModel):
    model: str | None = None
    messages: list[Message] = Field(
        min_length=1,
        max_length=20,
    )
    temperature: float | None = 0.0
    max_tokens: int | None = 300


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "model": OLLAMA_MODEL,
    }


@app.post("/v1/chat/completions")
async def chat(
    request: ChatRequest,
    authorization: str | None = Header(default=None),
):
    if authorization != f"Bearer {APP_API_KEY}":
        raise HTTPException(
            status_code=401,
            detail="unauthorized",
        )

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            *[
                message.model_dump()
                for message in request.messages
                if message.role != "system"
            ],
        ],
        "temperature": 0.0,
        "max_tokens": min(
            request.max_tokens or 300,
            300,
        ),
        "stream": False,
    }

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/chat/completions",
                headers={
                    "Authorization": "Bearer ollama",
                },
                json=payload,
            )

        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="model service unavailable",
        ) from exc

    return response.json()