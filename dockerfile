FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt
RUN pip install gunicorn
EXPOSE 5000
CMD [ "gunicorn", "-w", "2", "--bind", "0.0.0.0:5000", "app:app" ]