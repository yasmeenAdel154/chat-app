# crud.py
from sqlalchemy.orm import Session
from models import User, Interaction
import schemas
from typing import List, Optional

# Users
def create_user(db: Session, user_in: schemas.UserCreate) -> User:
    user = User(username=user_in.username, email=user_in.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def list_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

# Interactions
def create_interaction(db: Session, interaction_in: schemas.InteractionCreate) -> Interaction:
    interaction = Interaction(
        user_id=interaction_in.user_id,
        user_input=interaction_in.user_input,
        model_response=interaction_in.model_response
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction

def list_interactions(db: Session, user_id: int = None, skip: int = 0, limit: int = 100):
    q = db.query(Interaction)
    if user_id:
        q = q.filter(Interaction.user_id == user_id)
    return q.order_by(Interaction.created_at.desc()).offset(skip).limit(limit).all()

def get_interaction(db: Session, interaction_id: int):
    return db.query(Interaction).filter(Interaction.id == interaction_id).first()
