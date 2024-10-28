# Notes API
простой веб-сервис для хранения и управления текстовыми заметками

## Возможности
- Создание заметки
- Чтение заметки по её id
- Получение информации о времени создания и последнем обновлении заметки
- Обновление текста заметки
- Удаление заметки
- Вывод списка всех id заметок

## Используемые технологии
- Python
- FastAPI
- Pydantic
- Uvicorn
- JSON для хранения данных

Чтобы запустить сервер API выполните команду uvicorn main:app --reload
После запуска сервера получить доступ к документации API по адресу http://127.0.0.1:8000/docs
