#!/bin/sh
mongod -logpath /data/db/mongo.log -fork
spawn-fcgi -d /websites/WordPlatform-Beiyu -f /websites/WordPlatform-Beiyu/index.py -a 127.0.0.1 -p 9002
