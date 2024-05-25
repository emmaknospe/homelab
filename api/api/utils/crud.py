import typing

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Session

from db import get_db


class CRUDRouter(APIRouter):
    def __init__(self,
                 model: typing.Type[BaseModel],
                 create_model: typing.Type[BaseModel],
                 update_model: typing.Type[BaseModel],
                 sql_model: typing.Type[DeclarativeBase],
                 *args,
                 **kwargs):
        self.model = model
        self.create_model = create_model
        self.update_model = update_model
        self.sql_model = sql_model
        if not (prefix := kwargs.get("prefix")):
            prefix = f"/{sql_model.__tablename__}"
        kwargs["prefix"] = prefix
        super().__init__(*args, **kwargs)
        self._add_routes()

    def _add_routes(self):
        async def create_endpoint(item, db: Session=Depends(get_db)):
            db_item = self.sql_model(**item.dict())
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return self.model.model_validate(db_item)

        create_endpoint.__doc__ = f"Create a {self.model.__name__} item"
        create_endpoint.__annotations__ = {"item": self.create_model, "return": self.model}

        self.add_api_route(
            path="/",
            endpoint=create_endpoint,
            methods=["POST"],
        )

        async def read_endpoint(id: int, db: Session=Depends(get_db)):
            return self.model.model_validate(db.query(self.sql_model).get(id))

        read_endpoint.__doc__ = f"Read a {self.model.__name__} item"
        read_endpoint.__annotations__ = {"id": int, "return": self.model}

        self.add_api_route(
            path="/{id}",
            endpoint=read_endpoint,
            methods=["GET"],
        )

        async def update_endpoint(self, id: int, item, db: Session=Depends(get_db)):
            db_item = db.query(self.sql_model).get(id)
            for key, value in item.dict().items():
                setattr(db_item, key, value)
            db.commit()
            db.refresh(db_item)
            return self.model.model_validate(db_item)

        update_endpoint.__doc__ = f"Update a {self.model.__name__} item"
        update_endpoint.__annotations__ = {"id": int, "item": self.update_model, "return": self.model}

        self.add_api_route(
            path="/{id}",
            endpoint=update_endpoint,
            methods=["PUT"],
            response_model=self.model,
        )

        async def delete_endpoint(id: int, db: Session=Depends(get_db)):
            db_item = db.query(self.sql_model).get(id)
            db.delete(db_item)
            db.commit()
            return self.model.model_validate(db_item)

        delete_endpoint.__doc__ = f"Delete a {self.model.__name__} item"
        delete_endpoint.__annotations__ = {"id": int, "return": self.model}

        self.add_api_route(
            path="/{id}",
            endpoint=delete_endpoint,
            methods=["DELETE"],
        )

        async def list_endpoint(db: Session=Depends(get_db)):
            return [self.model.model_validate(item) for item in db.query(self.sql_model).all()]

        list_endpoint.__doc__ = f"List {self.model.__name__} items"
        list_endpoint.__annotations__ = {"return": list[self.model]}

        self.add_api_route(
            path="/",
            endpoint=list_endpoint,
            methods=["GET"],
        )
