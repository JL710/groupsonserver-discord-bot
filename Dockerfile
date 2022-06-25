FROM debian

RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install git+https://github.com/Rapptz/discord.py.git

ADD db.py /bot/db.py
ADD default_commands.py /bot/default_commands.py
ADD default.py /bot/default.py
ADD group_commands.py /bot/group_commands.py
ADD log.py /bot/log.py
ADD main.py /bot/main.py

WORKDIR /bot

CMD ["python3", "/bot/main.py"]