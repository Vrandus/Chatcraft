#!/bin/bash

screen -S mcserver -d -m java -Xms2048M -Xmx4192M -jar server.jar

cd Bot
screen -XS bot quit
screen -S bot -d -m python3.6 chatcraft.py

