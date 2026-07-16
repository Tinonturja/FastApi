from fastapi import FastAPI
import create_fastapi, put_delete
app = FastAPI()

app.include_router(create_fastapi.router)
app.include_router(put_delete.router)