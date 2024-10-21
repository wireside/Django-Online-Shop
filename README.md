# Lyceum
![pipeline](https://gitlab.crja72.ru/django/2024/autumn/course/students/248227-bogdansalaeff-course-1187/badges/main/pipeline.svg)
![Иллюстрация к проекту](https://gitlab.crja72.ru/django/2024/autumn/course/students/248227-bogdansalaeff-course-1187/-/blob/main/ER.jpg)
## Установите и активируйте виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate
```
## Установка зависимостей
```bash
pip install -r requirements/prod.txt
``` 
### Для разработки необходмио дополнительно установить зависмости из 
`requirements/dev.txt`
```bash
pip install -r requirements/dev.txt
``` 
### Для запусков тестов зависимости перечислены в `requirements/test.txt`
```bash
pip install -r requirements/test.txt
``` 
## Настройка переменных окружения
Скопируйте файл `config.env` в `.env`, если нужно, отредактируйте значения 
переменных.
```bash
cp config.env .env
```
## Запуск
```bash
cd lyceum
python3 manage.py runserver
```