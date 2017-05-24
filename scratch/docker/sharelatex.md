# Notes for sharelatex in docker
https://github.com/sharelatex/sharelatex/wiki

## run docker container
```bash
$ sudo docker run -d --name sharemongo --restart unless-stopped -v /var/sharemongo:/data/db mongo:latest (:2.6 - old sharelatex)

$ sudo docker run -d --name shareredis --restart unless-stopped -v /var/shareredis:/var/lib/redis redis:latest

$ sudo docker run -d -P -p 80:80 --restart unless-stopped -v /var/sharelatex:/var/lib/sharelatex  --env SHARELATEX_MONGO_URL=mongodb://mongo/sharelatex --env SHARELATEX_REDIS_HOST=redis --link sharemongo:mongo --link shareredis:redis --name sharelatex sharelatex/sharelatex
```

## update parameters of existing container
```bash
sudo docker update --restart=unless-stopped
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


sudo docker exec sharelatex /bin/bash -c "tail -50 /var/log/sharelatex/document-updater.log"
sudo docker exec sharelatex /bin/bash -c "tail -50 /var/log/sharelatex/clsi.log"
```
