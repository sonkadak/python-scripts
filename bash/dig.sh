#!/bin/bash
for i in {1..500}
do
	dig @8.8.8.8 DOMAIN.COM +noall +answer |grep odd |awk '{print $5}' |grep 175 >> result.txt
done
