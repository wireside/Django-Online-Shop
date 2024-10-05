# Lyceum
![Flake8]
![Black]
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