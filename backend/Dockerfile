FROM python:3.9-slim-buster

WORKDIR /task_manager

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]