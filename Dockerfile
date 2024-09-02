# Використовуємо базовий образ Python
FROM python:3.11-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файли конфігурації
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код проекту
COPY . .

# Виставляємо команду за замовчуванням
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]