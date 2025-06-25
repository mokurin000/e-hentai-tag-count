#!/usr/bin/env bash

sudo mariadb -u root <<< 'CREATE DATABASE IF NOT EXISTS `e-hentai-db`'
sudo mariadb -u root -p e-hentai-db < 2025_01_08.sql
