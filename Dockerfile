FROM fromang/py-mongo-service

### Prepare environment


# Variables
ENV PATH=$PATH:/usr/local/bin \
    HOME=/srv/

RUN apt install nginx-extras -y

# Copy config files
ADD docker /
WORKDIR /srv

# Install python packages
ADD requirements.txt /srv
RUN pip install -r requirements.txt

### Configure mongodb

EXPOSE 27017

### Configure nginx

# Remove default site
RUN rm -rf /etc/nginx/sites-enabled/default

# Link logs
RUN rm -rf /var/log/nginx
RUN ln -s /srv/data/log/nginx /var/log/

# Link lib
RUN rm -rf /var/lib/nginx
RUN ln -s /srv/data/lib/nginx /var/lib/

EXPOSE 8000

###

### Configure pasqua jove service

# Add server files
ADD src /srv/src

# Env variables
ENV PASQUAJOVE_DATABASE_NAME=pasquajove
ENV PASQUAJOVE_DATABASE_URL=mongodb://localhost:27017/

ENV PASQUAJOVE_MAIL_ADDRESS=someemail@gmail.com
ENV PASQUAJOVE_MAIL_PASSWORD=somepassword

ENV PASQUAJOVE_JWT_SECRET=supersercret

# !! Do not expose service port directly if you don't have a good reason
# use nginx port insted

# EXPOSE 5000

###

CMD ["init-service"]
