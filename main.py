from fastapi import FastAPI , Request,status
from .models import Base
from .database import engine 
from .routers import auth,todos,admin,users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="Todo/templates")

app.mount("/static",StaticFiles(directory="Todo/static"),name="static")

@app.get("/")
def test(request : Request):
    return RedirectResponse(url='/todo/todo-page',status_code=status.HTTP_302_FOUND)

@app.get("/healthy")
async def health_check():
    return {'status':'healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

