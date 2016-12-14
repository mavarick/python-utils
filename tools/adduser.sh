#!/bin/bash
if [ $# -eq 1 ];then
/usr/sbin/userdel $1;
/usr/sbin/groupdel $1;
/usr/sbin/useradd -g users $1;
/usr/bin/passwd -u $1;
/usr/bin/passwd -d $1;
/usr/bin/passwd -S $1;
echo "$1:*" |chpasswd -e
mkdir /home/$1
#mkdir /home/$1/.ssh;
#wget http://220.181.29.100/newkey/$1.key -O /home/$1/$1.key
#cat /home/$1/$1.key > /home/$1/.ssh/authorized_keys;
chown -R $1 /home/$1;
chgrp -R users /home/$1;
chmod 700 /home/$1;
#chmod 700 /home/$1/.ssh;
#chmod 600 /home/$1/.ssh/*;
#chown -R $1 /home/$1/.ssh;
#rm -f /home/$1/$1.key;
fi
