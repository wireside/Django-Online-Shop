# Lyceum
![pipeline](https://gitlab.crja72.ru/django/2024/autumn/course/students/248227-bogdansalaeff-course-1187/badges/main/pipeline.svg)
![coverage](https://gitlab.crja72.ru/django/2024/autumn/course/students/248227-bogdansalaeff-course-1187/badges/main/coverage.svg?job=linting)
### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
```
python -m venv venv
```
```
source venv/bin/activate
```
- Установите зависимости из файла requirements.txt
```
pip install -r requirements/prod.txt
``` 
- Создайте файл .env и задайте переменные окружения
```
touch .env
```
- В папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```