FROM mysql

ENV MYSQL_ROOT_PASSWORD root
ENV MYSQL_DATABASE echo_cardio
ENV MYSQL_USER tungluu18
ENV MYSQL_PASSWORD tungluu18

VOLUME [ "mysqldata:/var/lib/mysql" ]
