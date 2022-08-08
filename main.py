from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.datastruct.database import engine
from app.routers import authentication, uml, project, diagram, collaborator, invitation, version, alert, websocket, index
from app.datastruct import models, database
from dotenv import load_dotenv
from app.seeder import seeder
import uvicorn 
import os

#init
load_dotenv()
app = FastAPI(
    title="UMLDesigner API",
    description="An API for an AI-based uml diagram development assistant that processes technical specifications in natural language using NLP tools and return an xml file discribing generated uml schema structure."
)
models.Base.metadata.create_all(engine)

#cross origin
origins = [
    "http://localhost",
    "http://localhost:8080",
    ""
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#seeder
# seeder.init_db(next(database.get_db))

#routes
app.include_router(authentication.router)
app.include_router(project.router)
app.include_router(collaborator.router)
app.include_router(invitation.router)
app.include_router(diagram.router)
app.include_router(version.router)
app.include_router(alert.router)
app.include_router(uml.router)
app.include_router(websocket.router)
app.include_router(index.router)
app.include_router(seeder.router)

#main
if __name__ == "__main__":
    uvicorn.run("main:app", host=os.getenv('HOST'), port=int(os.getenv('PORT')), reload=os.getenv('AUTO_RELOAD'))

 
