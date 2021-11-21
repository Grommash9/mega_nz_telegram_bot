You should enter your id in config file, after this you are owner and you can add managers, you will have Add manager, Remove Manager, and Managers list buttons, nobody except you cant see or use it.

You asking id from you managers and adding them, after that whey can upload the files, also managers have Files List button to see the files.

For each manager will be create folder on mega by his telegram id, it is automated.

Manager should just drop the file to bot and bot ask for the new name, if manager already have file with that name in his folder - hi well receive an error about this.

Also if mega account doesn't work - manager will get an error about it - so he will be able to contact you and ask to change the account.

After uploading manager can get link by sending file name to the bot, also hi will be able to delete it from data base BUT not from the mega website.

Also files will be deleted from the server after upload

Бот для загрузки файлов на мегу. Есть супер админ, он добавляет менеджеров, менеджеры могут скидывать файлы, писать их навзание и файлы будут выгружены на мегу в папку с айдм менеджера (если такой нет - она будет создана автоматически) после этого файл удалиться с сервера. Название файла и ссылка на него будут добавлены в базу данных и в личный список менеджера, менеджеры не видят списков друг друга и не могут получать к ним доступ. По кнопке показать список файлов можно получить все имена и ссылки которые были загружены. Что бы удалить файл нужно обратиться к нему в чате бота, просто написав название, если файл с таким именем есть в бд - он появиться с кнопкой удаления. Файл удаляеться только из бд, с меги он не будет удален. Для обычных юзеров бот не доступен.

В файле конфига нужно прописать токен бота, айди главного админа, путь к базе данных и путь по которому будут лежать временные файлы.

Понятные проблемы на которые сознательно не обращаеться внимание:
- если не ввести имя файла он не будет удален из системы
- если список ссылкок или список менеджеров привысит 4096 символов он не будет разбит на сообщения и вообще ничего не выведеться
- также есть костыль, потому что софт писался срочно и не было времени разбираться с либой, перед работой с файлом он будет переименован в системе до выгрузки на мегу. 
- юзер без прав менеджера может отправить файл и он будет загружен на сервер. Нет понимания пока что как получить юзер айди во время принятия файла





![alt tag](https://github.com/Grommash9/mega_nz_telegram_bot/blob/master/images/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA1.PNG "")​
![alt tag](https://github.com/Grommash9/mega_nz_telegram_bot/blob/master/images/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA2.PNG "")​
![alt tag](https://github.com/Grommash9/mega_nz_telegram_bot/blob/master/images/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA3.PNG "")​
![alt tag](https://github.com/Grommash9/mega_nz_telegram_bot/blob/master/images/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA4.PNG "")​

