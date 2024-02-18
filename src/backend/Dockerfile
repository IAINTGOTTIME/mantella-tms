FROM python:3.10-alpine

RUN pip install pipenv

COPY . .

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

ENV PATH="/.venv/bin:$PATH"

CMD ["uvicorn", "mantella:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]

EXPOSE 8080