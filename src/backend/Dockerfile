FROM python:3.10-alpine AS build

RUN pip install pipenv

COPY . . 

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

ENV PATH="/.venv/bin:$PATH"

CMD ["sh", "-c", "alembic upgrade head && uvicorn mantella:app --host 0.0.0.0 --port 80 --proxy-headers"]

EXPOSE 8080
