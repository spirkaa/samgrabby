# SamGrabby

Парсер сайта samlab.ws и автоматически обновляемый список программ, которыми я пользовался на Windows.

Первая версия появилась в начале 2015 года на Flask, но чуть позже я начал изучать Django, поэтому мигрировал проект на него.

## Запуск prod

1. Переименовать файл `.env.example` в `.env`
1. Настроить переменные в файле `.env`
1. Последовательно выполнить команды

        docker compose up -d --build
        docker compose run django python manage.py migrate
        docker compose run django python manage.py createsuperuser
        docker compose run django python manage.py runjobs daily
