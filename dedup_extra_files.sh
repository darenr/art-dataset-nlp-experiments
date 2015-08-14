rm -f /tmp/aggregate
for f in extras/*.txt; do (tr '\n' ' ' <$f; echo) >> /tmp/aggregate; done
sort /tmp/aggregate | uniq -u > unique_extra_files.txt
rm -f /tmp/aggregate
