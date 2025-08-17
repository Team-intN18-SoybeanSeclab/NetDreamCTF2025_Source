FROM php:7.4-apache

USER root

COPY index.php /var/www/html/index.php

COPY start.sh /start.sh

RUN chmod +x /start.sh

CMD ["/start.sh"]