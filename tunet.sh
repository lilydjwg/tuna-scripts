#!/bin/bash
USER="username"
PASSWORD="password"
PASSWORD=`echo -n $PASSWORD|md5sum|cut -d' ' -f1`

curl 'https://net.tsinghua.edu.cn/do_login.php' -X 'POST' -H 'Origin: https://net.tsinghua.edu.cn' \
	--data "action=login&username=${USER}&password={MD5_HEX}${PASSWORD}&ac_id=1"
