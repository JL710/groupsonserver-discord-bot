# groupsonserver-discord-bot
A bot that allows custom group channels on a discord server.

```
docker build -t groupbot .
```

## running
```
docker run -d -v /mnt/e/temp/bottest/settings:/bot/settings -v /mnt/e/temp/bottest/log:/bot/log -v /mnt/e/temp/bottest/data:/bot/data groupbot
```