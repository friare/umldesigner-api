# python base image in the container from Docker Hub
FROM python:3.8.10-slim

# copy files to the /app folder in the container
COPY ./app /app/app
COPY ./main.py /app/main.py
COPY ./database.db /app/database.db
COPY ./requirements.txt /app/requirements.txt

ARG MAIL_USERNAME=null
ARG MAIL_PASSWORD=null
ARG MAIL_SERVER=null
ARG ADMIN_EMAIL=null
ARG ADMIN_PASSWORD=null

# set the working directory in the container to be /app
WORKDIR /app
SHELL ["/bin/bash", "-c"] 

# install the packages from the Pipfile in the container
RUN python -m venv api-env
RUN source api-env/bin/activate
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# expose the port that uvicorn will run the app on
ENV PORT=8000
EXPOSE 8000

ENV HOST=0.0.0.0
ENV AUTO_RELOAD=True

ENV MAIL_USERNAME=$MAIL_USERNAME
ENV MAIL_PASSWORD=$MAIL_PASSWORD
ENV MAIL_SERVER=$MAIL_SERVER
ENV ADMIN_EMAIL=$ADMIN_EMAIL
ENV ADMIN_PASSWORD=$ADMIN_PASSWORD



# execute the command python main.py (in the WORKDIR) to start the app
CMD ["python", "main.py"]
