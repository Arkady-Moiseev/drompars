# DROMPARS
<b>Целью проекта является изучение парсинга сайтов с помощью инструмента Selenium и дальнейшее использование полученых данных</b>
___
<b>Предполагается что БД Postgresql установлена и настроена. В скрипте необходимо добавить имя БД, имя пользователя и пароль, IP.</b>

<b>Необходимые пакеты и библиотеки:</b>

<i>yum install openssl11-devel (не работал pip без данной версии ssl)

pip3 install requests  

pip3 install selenium

pip3 install bs4

pip3 install keyboard

pip3 install psycopg2-binary</i>

Запуск скрипта:

Можно написать Unit файл или использовать Cron для периодического запуска - например <b>/etc/crontab:</b>

  <i>0 17 *  *  * root /usr/local/bin/python3 /opt/parsdrom/<a href="https://github.com/Arkady1996/drompars/blob/main/drom.py">drom.py</a> <b>1</b></i>

Для запуска скрипта необходимо передать параметр - номер необходимого региона

Поднять Grafana и настроить подключение к БД. Готовый <a href="https://github.com/Arkady1996/drompars/blob/main/jsonmodel">json дашборд.</a>

![img_1](https://github.com/Arkady1996/drompars/blob/main/images/drom_dashboard.PNG)
