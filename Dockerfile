FROM python:3.9

RUN mkdir -p /var/opt/app
WORKDIR /var/opt/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]
