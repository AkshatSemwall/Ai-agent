from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from backend.api.routes import router

app = FastAPI(title="AI Research & Report Agent")

app.include_router(router)
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/static/index.html")
