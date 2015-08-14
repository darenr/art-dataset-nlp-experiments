rm -f /tmp/aggregate
for f in extras/*.txt; do (tr '\n' ' ' <$f; echo) >> /tmp/aggregate; done
soirt | uniq -u /tmp/aggregate > unique_extra_files.txt
