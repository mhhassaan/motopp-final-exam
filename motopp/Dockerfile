FROM python:3.9-slim

WORKDIR /app

# requirements live in the motopp/ build context (compose sets build: ./motopp)
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app package
COPY . /app/motopp

# normalize run.sh and make executable if present
RUN if [ -f /app/motopp/run.sh ]; then sed -i 's/\r$//' /app/motopp/run.sh && chmod +x /app/motopp/run.sh; fi

ENV FLASK_APP=motopp
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV ENV=prod
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# prefer the project’s script if available; fall back to flask run
CMD [ "sh", "-c", "[ -x /app/motopp/run.sh ] && /app/motopp/run.sh || flask run" ]
