@echo off
call docker-compose restart postgres-app
call docker-compose restart postgres-auth
