FROM python:3.7

WORKDIR /usr/src/CryptoMonitor

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate

CMD [ "python", "manage.py", "runserver" ]
