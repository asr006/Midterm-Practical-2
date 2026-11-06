import random
from sqlmodel import select
from fastapi import APIRouter, HTTPException, status

from db import SessionDep
from models import Videos, VideosCreate

router = APIRouter(prefix="/videos")


@router.get("/")
def get_videos(session: SessionDep, categoria: str = ""):
    if categoria:
        return session.exec(select(Videos).where(Videos.categoria == categoria)).all()
    return session.exec(select(Videos)).all()


@router.get("/categorias")
def get_categorias(session: SessionDep):
    videos = session.exec(select(Videos)).all()
    categorias = []
    for video in videos:
        if video.categoria not in categorias:
            categorias.append(video.categoria)
    return categorias


@router.get("/{video_id}")
def get_video_by_id(video_id: int, session: SessionDep):
    video_db = session.get(Videos, video_id)
    if not video_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El video no fue encontrado"
        )
    return video_db


@router.get("/{video_id}/recomendaciones")
def get_recomendaciones(video_id: int, session: SessionDep):
    video_db = session.get(Videos, video_id)
    if not video_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El video no fue encontrado"
        )

    misma_categoria = list(session.exec(
        select(Videos).where(Videos.categoria == video_db.categoria, Videos.id != video_id)
    ).all())
    otras_categorias = list(session.exec(
        select(Videos).where(Videos.categoria != video_db.categoria)
    ).all())

    random.shuffle(misma_categoria)
    random.shuffle(otras_categorias)

    return (misma_categoria + otras_categorias)[:10]


@router.post("/")
def create_video(video_data: VideosCreate, session: SessionDep):
    video = Videos.model_validate(video_data.model_dump())
    session.add(video)
    session.commit()
    session.refresh(video)
    return video
