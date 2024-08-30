# ToDo_App
#### Тестовое задание 

## Для запуска проекта:
1.Создайте контейнеры с помощью команды "docker compose build"<br/>
2.Запустите проект с помощью команды "docker compose up"<br/>

## Для проверки работы
Для проверки работоспособности нужно зарегистрировать пользователя при помощи метода POST /user/register<br/>
Далее для создания заметки можно использовать метод POST /note, в Basic Auth нужно добавить логин и пароль указанный при регистрации.<br/>
Для получения всех заметок пользователя используется метод GET /notes, также нужна Basic Auth<br/>


### Используемы библиотеки
Все используемы библиотеки перечислены в файле "requirements.txt"
