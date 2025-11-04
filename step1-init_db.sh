#!/usr/bin/env bash

if [ -f .env ]
then source .env
fi

DB_USER=${DB_USER:-root}
DB_NAME=${DB_NAME:-"e-hentai-db"}

sudo mariadb -u ${DB_USER} <<< 'CREATE DATABASE IF NOT EXISTS `'${DB_NAME}'`'
sudo mariadb -u ${DB_USER} -p ${DB_NAME} < nightly.sql
