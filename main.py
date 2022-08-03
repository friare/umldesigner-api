from fastapi import FastAPI
from app.datastruct.database import engine
from app.routers import blog, user, authentication, uml, project, diagram, collaborator, invitation, version
from app.datastruct import models
import os
from dotenv import load_dotenv
import uvicorn 

load_dotenv()

app = FastAPI(
    title="UMLDesigner API",
    description="An API for an AI-based uml diagram development assistant that processes technical specifications in natural language using NLP tools and return an xml file discribing generated uml schema structure."
)
models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(project.router)
app.include_router(collaborator.router)
app.include_router(invitation.router)
app.include_router(diagram.router)
app.include_router(version.router)

# app.include_router(uml.router)
# app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=os.getenv('HOST'), port=int(os.getenv('PORT')), reload=os.getenv('AUTO_RELOAD'))

 