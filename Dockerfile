FROM python:3.12-slim

RUN mkdir /app

WORKDIR /app

# Installation dependencies
RUN pip install --upgrade pip
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

