# Notes for sharelatex in docker
https://github.com/sharelatex/sharelatex/wiki

## move /var/lib/docker to other location
https://linuxconfig.org/how-to-move-docker-s-default-var-lib-docker-to-another-directory-on-ubuntu-debian-linux

## run docker container
```bash
$ sudo docker run -d --name sharemongo --restart unless-stopped \
    -v /var/sharemongo:/data/db mongo:latest (:2.6 - old sharelatex)

$ sudo docker run -d --name shareredis --restart unless-stopped \
    -v /var/shareredis:/var/lib/redis redis:latest

$ sudo docker run -d -P -p 80:80 --restart unless-stopped \
    -v /var/sharelatex:/var/lib/sharelatex  \
    --env SHARELATEX_ADMIN_EMAIL=admin@email.cz \
    --env SHARELATEX_SITE_URL=sharelatex.url.com \
    --env SHARELATEX_MONGO_URL=mongodb://mongo/sharelatex \
    --env SHARELATEX_REDIS_HOST=redis --link sharemongo:mongo \
    --link shareredis:redis --name sharelatex sharelatex/sharelatex
```

## install latex
```bash
$ docker exec sharelatex tlmgr install scheme-full
```
- install Microsoft fonts for XeLaTeX (apt not working in the current docker *sudo apt install ttf-mscorefonts-installer*)
```bash
$ cd /tmp
$ wget http://ftp.us.debian.org/debian/pool/contrib/m/msttcorefonts/ttf-mscorefonts-installer_3.6_all.deb
$ sudo dpkg -i ttf-mscorefonts-installer_3.6_all.deb
```

## update parameters of existing container
```bash
sudo docker update --restart=unless-stopped
```

## commit docker container
- useful when changing parameters in *sudo docker run .... sharelatex/sharelatex*
- one would have to stop sharelatex container, remove container, run container with new paremeters and reinstall complete tlmgr
```bash
$ sudo docker commit sharelatex sharelatex_full
$ sudo docker run -d -P -p 127.0.0.1:3000:80 ... --name sharelatex sharelatex_full
```
## update docker image/container
- backup data, remove containers
- run docker containers
- sharelatex - install tlmgr, ...
```bash
$ sudo docker pull sharelatex/sharelatex
$ sudo docker pull redis
$ sudo docker pull mongo
```

## docker remove
- remove stopped container, -f running container
```bash
$ sudo docker stop sharelatex
$ sudo docker rm sharelatex
$ sudo docker rm -f sharelatex
```

## list info
- list images
```bash
$ sudo docker images 
```
- list running containers
```bash
$ sudo docker ps
```
- list all containers
```bash
$ sudo docker ps -a
```

## backup/migrate mongodb
save - mongodump
```bash
sudo docker exec sharemongo /bin/bash -c "mongodump --out /data/db/dump_new"
```
restore - mongorestore
```bash
sudo docker exec sharemongo /bin/bash -c "mongorestore /data/db/dump"
```

## backup/migrate redis
- copy /var/lib/redis/dump.rdb
```bash
sudo chown redis:redis /var/shareredis/dump.rdb ???
sudo chown www-data:www-data /var/shareredis/dump.rdb ???
sudo chmod 660 /var/shareredis/dump.rdb 
```


```bash
sudo docker ps -s
sudo docker images

sudo docker start shareredis (stop)
sudo docker start sharemongo (stop)
sudo docker rm sharelatex


sudo docker pull sharelatex/sharelatex

sudo docker exec sharelatex tlmgr install scheme-full
sudo docker exec -i -t sharelatex /bin/bash

chat.log  
docstore.log          
filestore.log      
real-time.log  
tags.log          
web.log
clsi.log  
document-updater.log  
notifications.log  
spelling.log   
track-changes.log
sudo docker exec sharelatex /bin/bash -c "tail -50 /var/log/sharelatex/document-updater.log"
sudo docker exec sharelatex /bin/bash -c "tail -50 /var/log/sharelatex/clsi.log"
```

## list all users
```shell
$ sudo docker exec -i -t sharemongo /bin/bash
$ mongoexport -d sharelatex -c users -f email --csv
```
