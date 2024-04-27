FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install --upgrade pip setuptools && \
    pip install Cython && \
    pip install -r requirements.txt

CMD ["python", "main.py"]