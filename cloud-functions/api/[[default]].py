"""
Python Cloud Function - FastAPI Framework
A high-performance serverless function using FastAPI with automatic OpenAPI docs.
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import time
import datetime

app = FastAPI(
    title="FastAPI Cloud Function",
    description="A high-performance serverless function using FastAPI",
    version="1.0.0"
)


# Pydantic models for request/response validation
class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class MessageResponse(BaseModel):
    message: str
    framework: str
    timestamp: float


class HealthResponse(BaseModel):
    status: str
    timestamp: float
    type: str


class SearchResult(BaseModel):
    id: int
    name: str
    score: float


class SearchResponse(BaseModel):
    query: str
    limit: int
    offset: int
    count: int
    results: List[SearchResult]


@app.get("/", response_model=MessageResponse)
async def index():
    """Root endpoint - returns greeting message."""
    return {
        "message": "Hello from FastAPI Cloud Function!",
        "framework": "FastAPI",
        "timestamp": time.time()
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "type": "fastapi_function"
    }


@app.get("/info")
async def info():
    """Function information endpoint."""
    return {
        "name": "FastAPI Cloud Function",
        "framework": "FastAPI",
        "description": "A high-performance serverless function using FastAPI with automatic OpenAPI docs",
        "features": [
            "Async/await support",
            "Automatic OpenAPI documentation",
            "Pydantic validation",
            "Type hints",
            "High performance (Starlette + Pydantic)"
        ]
    }


@app.get("/time")
async def get_time():
    """Return current server time."""
    now = datetime.datetime.now()
    return {
        "timestamp": time.time(),
        "iso": now.isoformat(),
        "formatted": now.strftime("%Y-%m-%d %H:%M:%S"),
    }


@app.api_route("/echo", methods=["GET", "POST"])
async def echo(msg: Optional[str] = Query(None)):
    """Echo request information."""
    return {
        "method": "GET/POST",
        "query": {"msg": msg} if msg else {},
        "timestamp": time.time()
    }


@app.post("/json")
async def handle_json(data: dict):
    """Handle JSON request body with automatic validation."""
    return {
        "message": "JSON received and parsed",
        "received": data,
        "keys": list(data.keys()),
    }


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get user by ID with automatic path parameter validation."""
    if user_id < 0:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    return {
        "id": user_id,
        "username": f"user_{user_id}",
        "email": f"user{user_id}@example.com"
    }


@app.post("/users", response_model=dict, status_code=201)
async def create_user(user: UserCreate):
    """Create a new user with Pydantic model validation."""
    return {
        "message": "User created",
        "user": {
            "id": 12345,
            "username": user.username,
            "email": user.email or "",
        }
    }


@app.get("/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=100, description="Number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """Search functionality with query parameter validation."""
    results = [
        SearchResult(id=i, name=f"Result {i}", score=round(0.95 - i * 0.08, 2))
        for i in range(offset, offset + min(limit, 10))
    ]
    
    return {
        "query": q,
        "limit": limit,
        "offset": offset,
        "count": len(results),
        "results": results
    }


# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Not Found"}
    )


@app.exception_handler(500)
async def server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error"}
    )
