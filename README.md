# Публикация комиксов в VK

[TODO: скачивание комиксы с сайта [xkcd.com](https://xkcd.com/) и постинг их в группе VK]

### Как установить

Python3 должен быть установлен. Затем используйте 'pip' (или 'pip3' если есть конфликт с Python2) для установки зависимостей:

```pip install -r requiriments.txt```

Рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html) для изоляции проекта.

### Пример выполнения программы

запуск 
```
main.py
```

### Настройка окружения

Перед запуском необходимо создать файл `.env` и внести в него переменные:

`VK_APP_ID` с id вашего приложения в вк. Нужно создать в разделе 'Мои приложения'

`VK_TOKEN` ваш ключ доступа пользователя, можно получить согласно документации [API_VK](https://vk.com/dev/implicit_flow_user)

`VK_GROUP_ID` id вашего канала в VK

### Цель проекта

Проект написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).

