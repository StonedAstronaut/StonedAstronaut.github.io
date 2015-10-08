title: Новые команды в Linux для старых решений
date: 2015-05-20 18:17:00
status: published
tags: linux

Собственно копипаста [отсюда](http://bneijt.nl/blog/post/new-linux-commands-for-old-habbits/)

***

### вместо *netstat* используем *ss*:

    :::bash
    ss -lpn

### вместо *ifconfig* используем *ip addr*:

Раньше для вкл/выкл определенного интерфейса использовали

    :::bash
    ifconfig eth0 up

теперь так:

    :::bash
    ip link set dev eth0 up

Для конфигурирования интерфейса:

    :::bash
    ifconfig eth0 10.0.0.2/16

теперь:

    :::bash
	ip addr dev eth0 add 10.0.0.2/16

### вместо *ps aux | grep ...* используем *pgrep -af*

	:::bash
	ps aux | grep rtorrent

теперь:

	:::bash
	pgrep -af rtorrent
