# Фильтрация шагов на Stepik
Задание на стажировку от JetBrains по направлению "Создание системы для перевода текстов на платформе Stepik".

## Установка
Приложение написано на Python 3.  
Необходимые библиотеки перечислены в `requirements.txt`. Их можно установить с помощью команды:
```
pip install -r requirements.txt
```
Приложение использует Memcached для кэширования результатов. Установить его можно скачав с официального [сайта](https://memcached.org/).

## Настройка
Все настройки производятся в файле `stepiktask/settings.py`.  

### Безопасность
**Важно** Обязательно замените ключ в `SECRET_KEY` на длинную случайную (не псевдо) строку.    

### Сторонние хосты
При размещении приложения на стороннем хосте, добавьте его в `ALLOWED_HOSTS`.  

### БД
Поскольку в проекте БД не используется, были оставлены настройки по умолчанию для SQLite3.  
Перед первым запуском примените миграции:
```
python manage.py migrate
```

### Debug
Секцию администратора и debug mode можно настроить соответсвенно переменными `ADMIN_AVAILABLE` и `DEBUG`.

### Memcached
Адрес, порт и время сохранения кэш-записи в Memcached можно изменить в переменной `CACHES`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'address:port',
        'TIMEOUT': 5 * 60, # in seconds
    }
}
```

## Запуск
Сначала запустите Memcached:
```
memcached
```
Далее запустите тестовый сервер (в production следует использовать настоящий сервер, например, [Gunicorn](http://gunicorn.org/)):
```
python manage.py runserver
```

## Load testing
К приложению приложен простой скрипт для генерации запросов к API `loadtest.py`:
```
usage: loadtest.py [-h] [-requests REQUESTS]

optional arguments:
  -h, --help          show this help message and exit
  -requests REQUESTS  Number of requests to generate
```
Для нагрузочного тестирования советуем использовать [vegeta](https://github.com/tsenart/vegeta).  
Тогда для проведения теста необходимо выполнить:
```
python loadtest.py -requests <requests count> | vegeta attack -lazy | vegeta report
```


## API
### `/api/steps/<step_type>?lesson=<lesson_id>`
#### Параметры
* `step_type` - тип шага для фильтрации. Поддерживается только `text`, для остальных будет возвращена ошибка
* `lesson_id` - id урока. Если он не валиден (не существует или не является числом), будет вовзвращена ошибка
#### Возвращает
JSON объект с полями:  
* `status` - "error" в случае ошибки, "success" иначе
* `message` - описание для `status`
* `ids` - массив id отфильтрованных шагов. Всегда пустой в случае ошибки
