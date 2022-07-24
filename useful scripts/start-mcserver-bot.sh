#!/bin/bash

screen -S mcserver -d -m java -Xms1G -Xmx1G --log-limit 50 -jar server.jar

cd Bot
screen -XS bot quit
screen -S bot -d -m python3.6 chatcraft.py

