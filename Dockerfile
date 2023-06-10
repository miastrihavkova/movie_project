FROM python:3.9
WORKDIR /movie_project
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP=project.py
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]