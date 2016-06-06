#!/bin/bash
#make copy of day's log for use
cp /home/quillaja/static.quillaja.net/palmer/scrape.log /home/quillaja/static.quillaja.net/palmer/img/archive/$(date +%F).log
#send day's log stats to email
python /home/quillaja/static.quillaja.net/palmer/logstats.py $(date +%F)
#make zip archive
zip -9 -m -j /home/quillaja/static.quillaja.net/palmer/img/archive/$(date +%F).zip /home/quillaja/static.quillaja.net/palmer/img/*.jpg /home/quillaja/static.quillaja.net/palmer/img/archive/$(date +%F).log
#store a copy of the day's log, unzipped, in the archive
mv /home/quillaja/static.quillaja.net/palmer/scrape.log /home/quillaja/static.quillaja.net/palmer/img/archive/$(date +%F).log
#restore empty log
touch /home/quillaja/static.quillaja.net/palmer/scrape.log