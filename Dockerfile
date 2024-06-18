FROM python:3.10-slim

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY /crm /usr/src/app/crm
COPY /telegram /usr/src/app/telegram
COPY /microCrm.db /usr/src/app/microCrm.db
COPY /openapi.json /usr/src/app/microCRM.json
COPY /micro_public_key.pem /usr/src/app/micro_public_key.pem

EXPOSE 3000

RUN ls -la /usr/src/app

CMD ["uvicorn", "crm.openapi_server.main:app", "--host", "0.0.0.0", "--port", "3000"]
