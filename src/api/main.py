from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router, init_engine

app = FastAPI(
    title="Library RAG API", 
    description="A Robust FastAPI backend with Phoenix tracing, Rate Limiting, and CORS.",
    version="1.0.0"
)

# Open up CORS so any JS Frontend can talk to this cleanly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In heavy prod, pin this to localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("🚀 App Starting Up...")
    
    # 1. Startup Phoenix Tracing
    print("📡 Booting Arize Phoenix...")
    try:
        from src.monitoring.phoenix_tracer import init_phoenix
        url = init_phoenix()
        print(f"✅ Dashboard Ready: {url}")
    except Exception as e:
        print(f"⚠️ Skipping Phoenix Integration: {e}")
        
    # 2. Boot Embeddings & LLM
    print("🧠 Booting LlamaIndex Engines into VRAM...")
    init_engine()
    print("✅ Ready to accept connections.")


# Attach the Secured Routes
app.include_router(router, prefix="/api/v1", tags=["RAG Application"])

if __name__ == "__main__":
    import uvicorn
    # When deployed to a live server, consider dropping reload=True
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
