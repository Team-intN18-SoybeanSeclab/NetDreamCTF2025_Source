FROM sakadonohito/php5.6.23-apache

# 复制所有必要文件
COPY ./html/ /var/www/html/
COPY ./apache2.conf /etc/apache2/apache2.conf
COPY ./php.ini /usr/local/etc/php/php.ini
COPY ./start.sh /start.sh

# 创建目录并设置权限
RUN mkdir -p /var/www/html/uploads && \
    chmod -R 755 /var/www/html/ && \
    chmod -R 777 /var/www/html/uploads && \
    chown -R www-data:www-data /var/www/html && \
    chmod +x /start.sh && \
    a2enmod rewrite

EXPOSE 81

# 使用启动脚本
CMD ["/start.sh"]