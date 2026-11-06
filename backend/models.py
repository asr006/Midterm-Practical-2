from sqlmodel import Field, SQLModel, Relationship


class Videos(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    canal: str
    categoria: str
    descripcion: str
    source: str
    miniatura: str
    vistas: int = 0
    likes: int = 0

    comments: list["Comments"] = Relationship(back_populates="video")


class VideosCreate(SQLModel):
    titulo: str
    canal: str
    categoria: str
    descripcion: str
    source: str
    miniatura: str


class Comments(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    autor: str
    texto: str
    fecha: str
    video_id: int = Field(foreign_key="videos.id")

    video: Videos | None = Relationship(back_populates="comments")


class CommentsCreate(SQLModel):
    autor: str
    texto: str
