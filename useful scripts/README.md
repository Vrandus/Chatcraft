# Scripts

## script directory structure example

The following scripts can be set up to be the following or edited to match your directory structure.

```
/home/
├───mcserver
│   └───apples
│       ├───Bot
│       │   ...
│       │   └───start.sh
│       ├───server.jar
│       └───start-minecraft-bot.sh
├───healthcheck.sh
├───start-bot.sh
└───start-minecraft.sh

...
```
## Cron

append the following to your crontab and start the cron service.  
```
# Run healthcheck.sh every minute
* * * * * /home/minecraft/healthcheck.sh
# Run a restart script for the discord bot every 3 hours
0 */3 * * * /home/minecraft/start-bot.sh

```
