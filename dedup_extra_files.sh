rm -f /tmp/aggregate
for f in extras/*.txt; do (tr '\n' ' ' <$f; echo) >> /tmp/aggregate; done
uniq -c /tmp/aggregate > unique_extra_files.txt
