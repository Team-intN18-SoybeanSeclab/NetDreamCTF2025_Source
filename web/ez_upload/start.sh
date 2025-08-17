#!/bin/bash

# 将 FLAG 写入文件
echo "$FLAG" > /flag
mkdir /var/www/html/uploads
chmod 777 /var/www/html/uploads
# 设置安全权限
chmod 444 /flag
chown www-data:www-data /flag

# 清除环境变量
unset FLAG

# 启动 Apache
exec apache2-foreground