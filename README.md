## UML Dev Asistant / API
by Généreux

### RUN
source api-env/bin/activate
pip3 install -r requirements.txt
uvicorn main:app --port 8000 --reload

### PAGE
localhost:8000/docs
localhost:8000/redoc
