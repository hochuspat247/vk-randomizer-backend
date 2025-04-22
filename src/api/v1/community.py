from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.models.community import Community as CommunityModel
from src.schemas.community import Community, CommunityCreate
from src.api.deps import get_db

router = APIRouter()

@router.post("/communities/", response_model=Community)
def create_community(community: CommunityCreate, db: Session = Depends(get_db)):
    db_community = CommunityModel(**community.dict())
    db.add(db_community)
    db.commit()
    db.refresh(db_community)
    return db_community

@router.get("/communities/{community_id}", response_model=Community)
def read_community(community_id: int, db: Session = Depends(get_db)):
    db_community = db.query(CommunityModel).filter(CommunityModel.id == community_id).first()
    if db_community is None:
        raise HTTPException(status_code=404, detail="Community not found")
    return db_community
