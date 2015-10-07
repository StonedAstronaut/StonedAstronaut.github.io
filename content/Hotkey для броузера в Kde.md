title: Hotkey для броузера в Kde
date: 2015-08-19 01:02:00
status: published
tags: linux

***

    :::bash
	/bin/bash -c "`xdg-settings get default-web-broswer | sed 's/.desktop//g'`"
