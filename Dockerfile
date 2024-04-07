FROM python:3.8-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install python-bidi arabic-reshaper
EXPOSE 5000
ENV FLASK_ENV=development
CMD ["python", "app.py"]