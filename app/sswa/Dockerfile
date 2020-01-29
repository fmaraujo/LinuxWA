#FROM python:3
 
#Contents of Dockerfile
#Dockerfile to build an image which supports testing our Qxf2 Page Object Model.
FROM ubuntu

#RUN apt-get install xvfb

# Essential tools and xvfb
RUN apt-get update && apt-get install -y \
    software-properties-common \
    unzip \
    curl \
    xvfb 
 
# Chrome browser to run the tests
RUN curl https://dl-ssl.google.com/linux/linux_signing_key.pub -o /tmp/google.pub \
    && cat /tmp/google.pub | apt-key add -; rm /tmp/google.pub \
    && echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google.list \
    && mkdir -p /usr/share/desktop-directories \
    && apt-get -y update && apt-get install -y google-chrome-stable
# Disable the SUID sandbox so that chrome can launch without being in a privileged container
RUN dpkg-divert --add --rename --divert /opt/google/chrome/google-chrome.real /opt/google/chrome/google-chrome \
    && echo "#!/bin/bash\nexec /opt/google/chrome/google-chrome.real --no-sandbox --disable-setuid-sandbox \"\$@\"" > /opt/google/chrome/google-chrome \
    && chmod 755 /opt/google/chrome/google-chrome

#http://chromedriver.storage.googleapis.com/2.45/chromedriver_linux64.zip
# Chrome Driver
RUN mkdir -p /opt/selenium \
    && curl https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_linux64.zip -o /opt/selenium/chromedriver_linux64.zip \
    && cd /opt/selenium; unzip /opt/selenium/chromedriver_linux64.zip; rm -rf chromedriver_linux64.zip; ln -fs /opt/selenium/chromedriver /usr/local/bin/chromedriver;
 
# python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-pip

RUN xdg-mime default google-chrome.desktop 'x-scheme-handler/whatsapp'

COPY Requirements.txt /
RUN pip3 install --upgrade setuptools
RUN pip install ez_setup
RUN pip3 install -r /Requirements.txt
RUN pip3 install connexion[swagger-ui]
RUN pip3 install PyAutoIt
COPY . /app
WORKDIR /app
EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD ["server.py"]