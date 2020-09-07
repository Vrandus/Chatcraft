#!/bin/bash

RUNNING=$(/usr/bin/lsof -i:25565 | grep minecraft)
BOT=$(screen -ls | grep bot)

LOGFILE="healthcheck_$(TZ=':America/Toronto' date '+%d-%m-%Y').log"

if [ -z "$RUNNING" ]; then
	echo "[$(TZ=':America/Toronto' date '+%d/%m/%Y %I:%M%p')] 'Minecraft server down. Attempting to restart...'" >> "$LOGFILE"
	./start-minecraft.sh
fi
if [ -z "$BOT" ]; then
	echo "[$(TZ=':America/Toronto' date '+%d/%m/%Y %I:%M%p')] 'Discord bot down. Attempting to restart...'" >> "$LOGFILE"
	./start-bot.sh
fi
