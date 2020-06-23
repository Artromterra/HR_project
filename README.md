# HR_project
### skillfactory final project
---
### Для развертывания пректа в Docker.

1. Скопировать репозиторий.
2. Собрать контейнеры командой: docker-compose build.
3. Запустить контейнеры: docker-compose up затем остановить.
4. Создать миграции: docker-compose run web python manage.py makemigrations.
5. Провести миграции БД: docker-compose run web python manage.py migrate.
6. Создать суперпользователя: docker-compose run web python manage.py createsuperuser.(если загружать фикстуры, то суперпользователя можно не создавать)
7. Загрузить фикстуры в БД: docker-compose run web python manage.py loaddata data.xml
8. Запустить контейнеры: docker-compose up.
***
Сайт работает по адресу 127.0.0.1:8000
В базе данных предустановлены пользователи: admin, пароль admin (суперпользователь), пользователь с обычными привилегиями: user1 - user1. Так же можно сосздать своего пользователя произвольно в шаблоне авторизации.
***
Тесты создаются в админке, результаты тестирования так же сохраняются в админке с логином тестируемого по каждому тесту отдельно. 

Сайт на heroku: [Нажмите чтобы перейти](https://hr-project-by-artrom.herokuapp.com/)

