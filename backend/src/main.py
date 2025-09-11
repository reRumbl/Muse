import uvicorn
from fastapi import FastAPI
from src.schemas import SuccessResponse
from src.company.router import router as company_router
from src.composition.router import router as composition_router
from src.ensemble.router import router as ensemble_router
from src.musician.router import router as musician_router
from src.performance.router import router as performance_router
from src.record.router import router as record_router
from src.release.router import router as release_router

# --- FastAPI App ---
app = FastAPI(
    title='Muse',
    description='Muse API',
    docs_url='/docs',
    redoc_url=None
)

# --- Routers ---
app.include_router(company_router)
app.include_router(composition_router)
app.include_router(ensemble_router)
app.include_router(musician_router)
app.include_router(performance_router)
app.include_router(record_router)
app.include_router(release_router)


# --- Root Endpoint ---
@app.get('/')
async def root():
    return SuccessResponse(message='This is Muse API')


# --- Entry Point ---
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
