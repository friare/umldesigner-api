from fastapi import FastAPI
from .database import engine
from .routers import blog, user, authentication, uml
from . import models

app = FastAPI(
    title="SmartUML",
    description="An API for an AI-based uml diagram development assistant that processes technical specifications in natural language using NLP tools and return an xml file discribing generated uml schema structure."
)
models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(uml.router)