#!/bin/sh

alembic upgrade head

uvicorn main:app --host 0.0.0.0 --port 9300 --ssl-certfile /literature/letsencrypt/live/api.linguisage.ru/fullchain.pem --ssl-keyfile /literature/letsencrypt/live/api.linguisage.ru/privkey.pem