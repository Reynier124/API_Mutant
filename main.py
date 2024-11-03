import uvicorn
from fastapi import FastAPI, HTTPException
from starlette import status
from starlette.responses import JSONResponse
import logging

from config.database import Database
from controllers.dna_controller import DnaController
from controllers.mutant_controller import MutantController
from controllers.normal_controller import NormalController
from repositories.base_repository_impl import InstanceNotFoundError
from controllers.health_check import router as health_check_controller
from services.dna_tester import DnaTester
from schemas.dna_schema import DnaSchema


def create_fastapi_app():
    fastapi_app = FastAPI()

    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Guardar logs en 'app.log'
        logging.StreamHandler()            # También mostrar logs en la consola
    ]
    )
    logger = logging.getLogger(__name__)

    @fastapi_app.exception_handler(InstanceNotFoundError)
    async def instance_not_found_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    dna_controller = DnaController()
    fastapi_app.include_router(dna_controller.router, prefix="/dna")

    dna_service = DnaTester()
    @fastapi_app.post("/mutant/")
    async def check_mutant(dna_schema:DnaSchema):
        dna = dna_schema.dna
        logger.info(f"Dna recibido: {dna}")
        if dna_service.isMutant(dna):
            logger.info(f"Es mutante")
            dna_type = "mutant"
            dna_controller.save_dna(dna=dna, dna_type=dna_type)
            return {"mutant":True}
        else:
            logger.info(f"Normal, supuestamente")
            dna_type = "normal"
            dna_controller.save_dna(dna=dna, dna_type=dna_type)
            raise HTTPException(status_code=403, detail="Not a mutant")
    
    mutant_controller = MutantController()
    normal_controller = NormalController()

    @fastapi_app.get('/stats')
    def stats():
        count_mutant_dna = len(mutant_controller.get_all())
        count_human_dna = len(normal_controller.get_all())
        ratio = count_mutant_dna / (count_human_dna + count_mutant_dna)

        return {
            "count_mutant_dna": count_mutant_dna,
            "count_human_dna": count_human_dna,
            "ratio": ratio
        }

    fastapi_app.include_router(health_check_controller, prefix="/health_check")

    return fastapi_app


def run_app(fastapi_app: FastAPI):
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)

app = create_fastapi_app()

"""
if __name__ == "__main__":
    db = Database()
    db.create_tables()
    run_app(app)"""