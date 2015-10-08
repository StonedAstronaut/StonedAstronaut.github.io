Title: LVM on LUKS на примере arch
Date: 2015-07-26 3:53:00
Tags: linux, crypt
Status: published

## Создаём разделы физические

Вот такая структура диска.

* `/dev/sda1 -> /boot`

* `/dev/sda2 -> LVM`

### Шифруем раздел LVM

    :::bash
    cryptsetup luksFormat -c aes-xts-plain64 -s 512 /dev/sda2

больше о параметрах шифрования см. [здесь](https://wiki.archlinux.org/index.php/Dm-crypt/Device_encryption#Encryption_options_for_LUKS_mode)

    :::bash
    cryptsetup open --type luks /dev/sda2 lvm

### Создаём разделы на LVM

создаём физический раздел LVM:

    :::bash
    pvcreate /dev/mapper/lvm

создаём группу разделов LVM:

    :::bash
    vgcreate MyStorage /dev/mapper/lvm

создаём логические разделы LVM:

    :::bash
    lvcreate -L 8G MyStorage -n swapvol
    lvcreate -L 15G MyStorage -n rootvol
    lvcreate -l +100%FREE MyStorage -n homevol

форматируем разделы:

    :::bash
    mkfs.ext4 /dev/mapper/MyStorage-rootvol
	mkfs.ext4 /dev/mapper/MyStorage-homevol
	mkswap /dev/mapper/MyStorage-swapvol

наконец-то монтируем

    :::bash
    mount /dev/MyStorage/rootvol /mnt
    mkdir /mnt/home
    mount /dev/MyStorage/homevol /mnt/home
    swapon /dev/MyStorage/swapvol

### подготавливаем boot

    :::bash
    mkfs.ext2 /dev/sda1
	mkdir /mnt/boot
	mount /dev/sda1 /mnt/boot

Дальше идёт обычная установка системы, до момента генерации **initramfs**.

Для того, что бы можно было загружаться с lvm надо добавить в `/etc/mkinitcpio.conf`:

    :::bash
    /etc/mkinitcpio.conf:
	HOOKS="... encrypt lvm2 resume ... filesystems ..."

**encrypted**, **lvm2** и **resume** должны стоять перед **filesystems**

### конфигурация загрузчика

Перед генерацией конфига *grub*, необходимо добавить информацию о зашифрованных разделах в `/etc/default/grub`:

    :::bash
    ...
	GRUB_CMDLINE_LINUX_DEFAULT="quiet resume=/dev/MyStorage/swapvol"
	GRUB_CMDLINE_LINUX="cryptdevice=/dev/sda2:MyStorage \
	root=/dev/mapper/MyStorage-rootvol"
	...

Собственно всё.

[ссылка на оригинал](https://wiki.archlinux.org/index.php/Dm-crypt/Encrypting_an_entire_system#LUKS_on_LVM)
