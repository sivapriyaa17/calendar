


'''from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.agent import agent_book  # make sure this import is correct

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/chat")
async def chat(req: Request):
    try:
        body = await req.body()
        print("📥 Raw request body:", body)

        data = await req.json()
        print("✅ Parsed JSON data:", data)

        user_input = data.get("message")
        if not user_input:
            return {"error": "Missing 'message' in request body"}

        result = agent_book.invoke(user_input)
        return {"response": result}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"Internal server error: {str(e)}"}'''
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.agent import calendar_agent

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Backend running"}
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/chat")
async def chat(req: Request):
    try:
        body = await req.body()
        print("📥 Raw request body:", body)

        data = await req.json()
        print("✅ Parsed JSON data:", data)

        user_input = data.get("message")
        print("📝 User message received:", user_input)

        if not user_input:
            return {"error": "Missing 'message' in request body"}

        result = calendar_agent.invoke({"input": user_input})
        return {"response": result}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"Internal server error: {str(e)}"}


