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
docker run -d -v ./settings:/bot/settings -v ./log:/bot/log -v ./data:/bot/data --restart unless-stopped groupbot
```