#!/bin/bash

#while read x;

xx=$(zcat $1 -f | cut -f 7 -d ' ' | grep /search?q= | cut -d'=' -f 2)
#echo $xx
#echo "==="

urldecode() { : "${*//+/ }"; echo -e "${_//%/\\x}"; }

res=""
#x="http%3A%2F%2Fstackoverflow.com%2Fsearch%3Fq%3Durldecode%2Bbash"
for x in `echo $xx`; do
	y=$(urldecode "$x")
	res="$res$y
"
#echo $x
#echo $y
done

#echo "====="
echo "$res" | grep -v "^$" | sort | uniq -c
