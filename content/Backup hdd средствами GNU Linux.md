title: Backup hdd средствами GNU/Linux
date: 2015-02-09 19:30:00
Tags: habr, linux, backup
Status: published

После теста hdd можно определить, пора ли менять диск или нет.

Если время пришло, то тогда необходимо перенести со старого жесткого всю инфу на новый.

Из гуглежа, стало ясно, чо использование обычного dd не "кошегно". Ъ использовать **GNU ddrescue**. Команда для backup'а выглядит следующим образом:

	:::bash
	# ddrescue /dev/sdX /pth_to_backup/disk.img /pth_to_backup/disk.img.log

Можно делать backup как раздела, так и всего hdd.

Для просмотра содержимого **раздела** используем следующую команду:

	:::bash
	# mount -o loop /pth_to_backup/drive.img /mnt

А для **образа физического диска**:

	:::bash
	# losetup --partscan /dev/loop0 drive.img
	# mount /dev/loop0p2 /mnt

или,

	:::bash
	# kpartx -a /dev/loop0 drive.img
	# mount /dev/mapper/loop0p2 /mnt

в зависимости от дистра.

Восстановление из образа:

	:::bash
	# ddrescue --force disk.img /dev/sdxX disk.img.log

!!!**раздел на который идет восстановление должен быть *НЕ* меньше файла-образа**

стырено [изхабра](http://habrahabr.ru/post/233961/)
