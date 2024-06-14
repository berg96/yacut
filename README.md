# Проект YaCut 

## Описание проекта 

На большинстве сайтов адреса страниц довольно длинные. Делиться такими длинными ссылками не всегда удобно, а иногда и вовсе невозможно. 
Удобнее использовать короткие ссылки. Например, ссылки https://yacut.ddns.net/zarabotoz или https://yacut.ddns.net/12e07d воспринимаются лучше, чем https://checkroi.ru/blog/kak-zarabotat-studentu-v-internete/#Zarabotok_na_kopirajtinge_i_rerajtinge. 

Проект [YaCut](https://yacut.ddns.net/)([https://yacut.ddns.net/](https://yacut.ddns.net/)) — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

Также у проекта есть API с тем же функционалом. Можно как создать короткую ссылку, так и получить оригинальную по короткой.

[Документация API](https://yacut.ddns.net/api/docs/)


### Автор backend Артём Куликов

tg: [@Berg1005](https://t.me/berg1005)

[GitHub](https://github.com/berg96)

## Используемые технологии 

Проект использует базу данных PostgreSQL для хранения данных и реализован на языке python c использованием следующих библиотек:

* Flask (v 3.0.2) 
* Flask-SQLAlchemy(v 3.1.1)
* Flask-Migrate (v 4.0.5) 
* alembic (v 1.12.0) 
* Flask-WTF (v 1.2.1)
* psycopg2 (v 2.9.9)
* flask_swagger_ui (v 4.11.1)
* gunicorn (v 22.0.0)


## Как запустить проект
Клонировать репозиторий:

```
git clone https://github.com/berg96/yacut.git
```

Перейти в него в командной строке:
```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip

pip install -r requirements.txt
```

Применить миграции:

```
flask db upgrade
```

Запустить сервер:

```
flask run
```
Документация API при запущенном сервере:

[http://127.0.0.1:5000/api/docs/](https://yacut.ddns.net/api/docs/)
