from datetime import datetime
from sqlmodel import select
from fastapi import APIRouter, HTTPException, status

from db import SessionDep
from models import Videos, Comments, CommentsCreate

router = APIRouter(prefix="/comments")


@router.get("/{video_id}")
def get_comments(video_id: int, session: SessionDep):
    video_db = session.get(Videos, video_id)
    if not video_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El video no fue encontrado"
        )
    return session.exec(
        select(Comments).where(Comments.video_id == video_id).order_by(Comments.id.desc())
    ).all()


@router.post("/{video_id}")
def create_comment(video_id: int, comment_data: CommentsCreate, session: SessionDep):
    video_db = session.get(Videos, video_id)
    if not video_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El video no fue encontrado"
        )
    comment = Comments(
        autor=comment_data.autor,
        texto=comment_data.texto,
        fecha=datetime.now().strftime("%d/%m/%Y %H:%M"),
        video_id=video_id,
    )
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment
