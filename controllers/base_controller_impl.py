from typing import Type, List
from flask import Blueprint, jsonify, request, abort
from controllers.base_controller import BaseController
from schemas.base_schema import BaseSchema
from services.base_service import BaseService

class BaseControllerImpl(BaseController):
    """Base controller implementation."""

    def __init__(self, schema: Type[BaseSchema], service: BaseService):
        self.service = service
        self.schema = schema
        self.blueprint = Blueprint('base', __name__)

        self.blueprint.add_url_rule("/", view_func=self.get_all, methods=["GET"])
        self.blueprint.add_url_rule("/<int:id_key>", view_func=self.get_one, methods=["GET"])
        self.blueprint.add_url_rule("/", view_func=self.save, methods=["POST"])
        self.blueprint.add_url_rule("/<int:id_key>", view_func=self.update, methods=["PUT"])
        self.blueprint.add_url_rule("/<int:id_key>", view_func=self.delete, methods=["DELETE"])

        def get_all(self):
            items = self.service.get_all()
            return jsonify([self.schema.from_orm(item).dict() for item in items])

        def get_one(self, id_key: int):
            item = self.service.get_one(id_key)
            if item is None:
                abort(404, description="Item not found")
            return self.schema.from_orm(item).dict()

        def save(self):
            schema_in = self.schema(**request.get_json())
            item = self.service.save(schema_in)
            return self.schema.from_orm(item).dict()

        def update(self, id_key: int):
            schema_in = self.schema(**request.get_json())
            item = self.service.update(id_key, schema_in)
            if item is None:
                abort(404, description="Item not found")
            return self.schema.from_orm(item).dict()

        def delete(self, id_key: int):
            self.service.delete(id_key)
            return "", 204


    @property
    def service(self) -> BaseService:
        """Service to access database."""
        return self._service

    @property
    def schema(self) -> Type[BaseSchema]:
        """Pydantic Schema to validate data."""
        return self._schema

    def get_all(self) -> List[BaseSchema]:
        """Get all data."""
        return self.service.get_all()

    def get_one(self, id_key: int) -> BaseSchema:
        """Get one data."""
        return self.service.get_one(id_key)

    def save(self, schema: BaseSchema) -> BaseSchema:
        """Save data."""
        return self.service.save(schema)

    def update(self, id_key: int, schema: BaseSchema) -> BaseSchema:
        """Update data."""
        return self.service.update(id_key, schema)

    def delete(self, id_key: int) -> None:
        """Delete data."""
        self.service.delete(id_key)

    @schema.setter
    def schema(self, value):
        self._schema = value

    @service.setter
    def service(self, value):
        self._service = value
