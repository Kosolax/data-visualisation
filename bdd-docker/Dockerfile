FROM mysql
ENV DB_DOCKER_PORT 3306

# docker run all sql script in /docker-entrypoint-initdb.d directory after mysql server is initialised
ADD myscript.sql /docker-entrypoint-initdb.d
EXPOSE ${DB_DOCKER_PORT}