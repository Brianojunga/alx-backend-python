FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /home/app

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /home/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]