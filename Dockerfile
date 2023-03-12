FROM python:3.9

WORKDIR /src

COPY requirements.txt /src/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY . /src/

EXPOSE 8000

CMD ["uvicorn", "core.asgi:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]