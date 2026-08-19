import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse

app = FastAPI()


ROUTER_URL = "https://api.b.ai/v1/chat/completions"  
TARGET_MODEL = (  
    "bai/deepseek-v4-flash"
)
INTERNAL_9ROUTER_KEY = (  
    "your-internal-key"
)
PUBLIC_API_KEY = (  
    "sk-dhodho-free-23691263gioug9e09812ye018"
)

@app.get("/v1/models")
async def list_models(request: Request):
  
  auth_header = request.headers.get("Authorization")
  if auth_header != f"Bearer {PUBLIC_API_KEY}":
    raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

  
  return {
      "object": "list",
      "data": [
          {
              "id": TARGET_MODEL,
              "object": "model",
              "created": 1677610602,
              "owned_by": "custom-router",
          }
      ],
  }

@app.post("/v1/chat/completions")
async def proxy_chat(request: Request):
  
  auth_header = request.headers.get("Authorization")
  if auth_header != f"Bearer {PUBLIC_API_KEY}":
    raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

  body = await request.json()
 
  body["model"] = TARGET_MODEL

  client = httpx.AsyncClient(timeout=120.0)

  async def response_generator():
    try:
      async with client.stream(
          "POST",
          ROUTER_URL,
          json=body,
          headers={"Authorization": f"Bearer {INTERNAL_9ROUTER_KEY}"},
      ) as response:
        async for chunk in response.aiter_bytes():
          yield chunk
    finally:
      await client.aclose()

  is_stream = body.get("stream", False)
  return StreamingResponse(
      response_generator(),
      media_type="text/event-stream" if is_stream else "application/json",
  )
