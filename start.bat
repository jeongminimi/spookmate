@echo off
title SpookMate Backend Server
cd /d C:\spookmate
call .venv\Scripts\activate
uvicorn app:app --reload --port 8000
pause