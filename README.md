# DROMPARS
Целью проекта является изучение парсинга сайтов с помощью инструмента Selenium
___
<b>Предполагается что БД Postgresql установлена и настроена</b>

<b>Необходимые пакеты и библиотеки:</b>

<i>yum install openssl11-devel

pip3 install requests  

pip3 install selenium

pip3 install bs4

pip3 install keyboard

pip3 install psycopg2-binary</i>

Запуск скрипта:

Можно написать Unit файлы или использовать Cron для периодического запуска - например <b>/etc/crontab:</b>

  <i>0 17 *  *  * root /usr/local/bin/python3 /opt/parsdrom/drom.py 1</i>

Для запуска скрипта необходимо передать параметр - номер необходимого региона

Поднять Grafana и настроить подключение к БД. Готовый <a href="https://github.com/Arkady1996/drompars/blob/main/jsonmodel">json дашборд.</a>

![img_1](https://github.com/Arkady1996/drompars/blob/main/images/drom_dashboard.PNG)
