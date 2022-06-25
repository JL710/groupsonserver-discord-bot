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
docker run -d -v YOUTPATH:/bot/settings -v YOURPATH:/bot/log -v YOURPATH:/bot/data groupbot
```