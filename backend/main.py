from fastapi import FastAPI
from routers import chat, crud
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers import chat
from routers import crud

app = FastAPI()
app.include_router(chat.router)
app.include_router(crud.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)