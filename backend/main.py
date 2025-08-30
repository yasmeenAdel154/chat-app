# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from database import engine, Base, get_db
import models, crud, schemas
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from agent import generate_response
# Create DB tables (for a simple task - replace with Alembic in prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Agent Backend")

# Allow front-end (Next.js dev) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # adjust or use ["*"] for test
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health
@app.get("/health")
def health():
    return {"status": "ok"}

# ---- Users ----
@app.post("/users/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_username(db, user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="username already exists")
    user = crud.create_user(db, user_in)
    return user

@app.get("/users/", response_model=List[schemas.UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_users(db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

# ---- Interactions ----
@app.post("/interactions/", response_model=schemas.InteractionRead, status_code=status.HTTP_201_CREATED)
def create_interaction(interaction_in: schemas.InteractionCreate, db: Session = Depends(get_db)):
    # ensure user exists
    user = crud.get_user(db, interaction_in.user_id)
    if not user:
        raise HTTPException(status_code=400, detail="invalid user_id")
    interaction = crud.create_interaction(db, interaction_in)
    return interaction

@app.get("/interactions/", response_model=List[schemas.InteractionRead])
def read_interactions(user_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_interactions(db, user_id=user_id, skip=skip, limit=limit)

@app.get("/interactions/{interaction_id}", response_model=schemas.InteractionRead)
def read_interaction(interaction_id: int, db: Session = Depends(get_db)):
    inter = crud.get_interaction(db, interaction_id)
    if not inter:
        raise HTTPException(status_code=404, detail="interaction not found")
    return inter

# ----- Chat with LLM -----
@app.post("/chat", response_model=schemas.ChatResponse)
def chat(req: schemas.ChatRequest, db: Session = Depends(get_db)):
    """
    1) Validate user exists.
    2) Call LLM to get reply.
    3) Store in interactions table.
    4) Return reply + interaction id.
    """
    user = crud.get_user(db, req.user_id)
    if not user:
        raise HTTPException(status_code=400, detail="invalid user_id")

    reply = generate_response(req.message)

    # Persist
    inter = crud.create_interaction(db, schemas.InteractionCreate(
        user_id=req.user_id,
        user_input=req.message,
        model_response=reply
    ))

    return schemas.ChatResponse(interaction_id=inter.id, reply=reply)
