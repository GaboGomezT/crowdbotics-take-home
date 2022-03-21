from fastapi import HTTPException
from sqlalchemy import table
from sqlmodel import Session, SQLModel, select


class CRUD(SQLModel):
    def save(self, session: Session):
        session.add(self)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session: Session):
        session.delete(self)
        session.commit()

    @classmethod
    def get_all(cls, session: Session):
        return session.exec(select(cls)).all()

    @classmethod
    def find(cls, id: int, session: Session):
        obj = session.get(cls, id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"{cls.__name__} not found")
        return obj
