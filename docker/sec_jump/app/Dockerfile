FROM python

WORKDIR /app

COPY . /app

RUN mkdir uploads

RUN pip install flask

EXPOSE 80
ENTRYPOINT ["python", "app.py"]
