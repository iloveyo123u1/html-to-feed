FROM base/archlinux:latest
MAINTAINER Stefan Koch

RUN pacman -Sy --noconfirm archlinux-keyring
RUN pacman-key --populate archlinux
RUN pacman -Sy --noconfirm
RUN pacman-db-upgrade
RUN pacman -S --noconfirm git openssl python-pip python-virtualenv libxml2 libxslt gcc
WORKDIR /opt
RUN git clone https://github.com/aufziehvogel/html-to-feed.git
WORKDIR /opt/html-to-feed
RUN virtualenv env
RUN source env/bin/activate
RUN pip install -r requirements.txt

# Workaround to get debug mode of website listen to all remote IPs
# without exposing this behaviour in other code
RUN printf "import website\nwebsite.app.run(host='0.0.0.0')" > run.py
RUN python run.py
