FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


RUN if [ ! -f "src/seed_data.py" ]; then echo "ERROR: src/seed_data.py not found!"; exit 1; fi


RUN python src/seed_data.py

EXPOSE 8000

CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0", "--port", "8000"]

