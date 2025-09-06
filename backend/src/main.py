import uvicorn
from fastapi import FastAPI
from schemas import SuccessResponse

# --- FastAPI App ---
app = FastAPI(
    title='Muse',
    description='Muse API',
    docs_url='/docs',
    redoc_url=None
)


@app.get('/')
async def root():
    return SuccessResponse(message='This is Muse API')


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
