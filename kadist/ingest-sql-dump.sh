rm -f ~/Dropbox/Kadist/kadist.db
cat ~/Dropbox/Kadist/dump.sql post_load_script.sql | sqlite3 ~/Dropbox/Kadist/kadist.db
