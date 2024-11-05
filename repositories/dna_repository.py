from models.dna import DnaModel
from repositories.base_repository_impl import BaseRepositoryImpl
from schemas.dna_schema import DnaSchema


class DnaRepository(BaseRepositoryImpl):
    def __init__(self):
        super().__init__(DnaModel, DnaSchema)