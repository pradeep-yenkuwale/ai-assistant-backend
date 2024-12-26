from fastapi import Request, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from app.routes import user, ticket
from app.middleware.global_exception.global_exception_middleware import exceptions_middleware 

app = FastAPI()

from platform import python_version
print("Current Python Version", python_version())

# Add routes to the server
app.include_router(user.router, prefix="/api")
app.include_router(ticket.router, prefix="/api")

@app.middleware("http")
async def enforce_https_middleware(request: Request, call_next):
    x_forwarded_proto = request.headers.get("x-forwarded-proto")
    print("x_forwarded_proto", x_forwarded_proto)
    if x_forwarded_proto == "https":
        request.scope["scheme"] = "https"
    response = await call_next(request)
    return response

# Mount static content to load on root call
app.mount("/static", StaticFiles(directory=os.path.join("app", "static")), name="static")

# Set the template
templates = Jinja2Templates(directory=os.path.join("app", "templates"))

# Render HTML file on root call
@app.get("/", response_description="Retrieved response")
async def load_template(request: Request):
    return templates.TemplateResponse("user_assistant.html", {"request": request})