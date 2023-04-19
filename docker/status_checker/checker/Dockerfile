FROM python

RUN apt update && apt install -y iputils-ping

WORKDIR /app

COPY . /app

RUN mkdir templates
RUN pip install flask

EXPOSE 8080
ENTRYPOINT ["python", "app.py"]
