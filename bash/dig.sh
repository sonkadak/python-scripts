#!/bin/bash
# bash script to find host which is not pinged correctly from DNS record txt file

# find the host on record
while IFS= read -r address
do
	dig +noall +answer "$address" |awk '{print $5}' >> hosttoping
done < /CNAME.txt

# find the host which is pinged or not
while IFS= read -r host
do
	if ! ping -oc 1 -W 3 $host &> /dev/null
	then
		echo "$host: Ping Failed"
		cat /DOMAIN.txt |grep $host |awk '{print $0}' >> ping-failed.txt
	else
		cat /DOMAIN.txt |grep $host |awk '{print $0}' >> pinged.txt
	fi
done < hosttoping
rm -f hosttoping
