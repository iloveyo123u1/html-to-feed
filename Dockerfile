FROM base/archlinux:latest
MAINTAINER Stefan Koch

RUN pacman -Sy && pacman -S --noconfirm \
    gcc \
    git \
    libxml2 \
    libxslt \
    openssl \
    python-pip \
    python-virtualenv
WORKDIR /opt
RUN git clone https://github.com/aufziehvogel/html-to-feed.git && \
    cd html-to-feed && \
    virtualenv env && \
    source env/bin/activate && \
    pip install -r requirements.txt

WORKDIR /opt/html-to-feed
# Workaround to get debug mode of website listen to all remote IPs
# without exposing this behaviour in other code
RUN printf "import website\nwebsite.app.run(host='0.0.0.0')" > run.py
RUN source env/bin/activate && python run.py
