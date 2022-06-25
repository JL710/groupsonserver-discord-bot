# groupsonserver-discord-bot
A bot that allows custom group channels on a discord server.


## build
```
docker build -t groupbot .
```

## Settings/
settings/settings.json
```
{
    "log-dir": "log",
    "data-dir": "data",
    "database": "data/database.db",
    "dm_endpoint_users": [],
    "default-category": "Groups",
    "custom-categorys": {}
}
```

settings/token
```
TOKEN HERE
```


## running
```
docker run -d -v /mnt/e/temp/bottest/settings:/bot/settings -v /mnt/e/temp/bottest/log:/bot/log -v /mnt/e/temp/bottest/data:/bot/data groupbot
```