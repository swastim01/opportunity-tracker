from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tracker import process_program

app = FastAPI()

# Enable CORS so React frontend can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class Query(BaseModel):
    program: str
    email: str

# Routes
@app.post("/analyze")
async def analyze_program(query: Query):
    try:
        result = process_program(query.program, query.email)
        return result
    except Exception as e:
        return {"error": str(e)}
