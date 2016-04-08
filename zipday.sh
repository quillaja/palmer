#!/bin/bash
#make zip archive
cp /home/quillaja/static.quillaja.net/palmer/scrape.log /home/quillaja/static.quillaja.net/palmer/img/archive/$(date +%F).log
zip -9 -m -j /home/quillaja/static.quillaja.net/palmer/img/archive/$(date +%F).zip /home/quillaja/static.quillaja.net/palmer/img/*.jpg /home/quillaja/static.quillaja.net/palmer/scrape.log
#restore empty log
touch /home/quillaja/static.quillaja.net/palmer/scrape.log
#send day's log stats to email
python /home/quillaja/static.quillaja.net/palmer/logstats.py $(date +%F)