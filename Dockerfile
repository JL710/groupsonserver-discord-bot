FROM debian

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y pip3
RUN pip3 install -y git+https://github.com/Rapptz/discord.py.git

ADD db.py
ADD default_commands.py
ADD default.py
ADD group_commands.py
ADD log.py
ADD main.py
ADD settings.json