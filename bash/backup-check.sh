#!/usr/bin/env bash
# Check the backup files made from K8S Cronjob "*-backup"
echo "Script version test:0.0.8d"
WORK_DIR="/tmp/backup"
cd "$WORK_DIR"

# slack webhook url
WEB_HOOK='URL'

BU_DATE=$(date -d "yesterday" |awk '{print $2,$3}')
COMP_DATE=$(date -d "2 days ago" |awk '{print $2,$3}')
BACKUP_CHK_LIST=(bugs gogs mysql psql wiki)

# compare file size with two backup files(2 days ago and a day ago)
function comp {
	fn=$1
	echo "comp "$fn
	target=$(ls -l |grep "$BU_DATE" |grep $fn |awk '{print $9}')
	echo "Backup file: "$target
	chk=$(ls -l |grep "$target" |awk '{print $5}')
	if [ $chk -le 0 ]
	then
		echo "No file detected."
		return 1
	fi
	case $target in
		*zip)
			echo "zip file detected";;
		*gz)
			echo "gz file detected";;
		*)
			echo "None zip or gz file. escaping..."
			return 1
	esac

        AGO=$(ls -l |grep "$target" |awk '{print $5}')
        AGO_COMP=$(ls -l |grep "$COMP_DATE" |grep "$fn" |awk '{print $5}')

        res=$(awk -v ago=$AGO -v comp=$AGO_COMP 'BEGIN {print (comp - ago)}')
        # absolute
	diff=$(awk -v r=$res 'BEGIN {if(r<0) {print sqrt(r*r)} else print r}')

        half=$(awk -v ago="$AGO" 'BEGIN {print (ago / 2)}')
	echo "File size: "$AGO
	echo "Difference: "$diff

	chk=$(awk -v ago=$AGO -v comp=$AGO_COMP -v d=$diff -v h=$half 'BEGIN {if((ago<comp) && (d>h)) print 0}')
	if [ "$chk" == "0" ]
	then
                msg=$msg" WARN: \```$ent\/$target\```: size difference more than 50%: $diff Bytes. (File size: $AGO Bytes\r\n"
        fi
}

# loop each backup directory
for ent in "${BACKUP_CHK_LIST[@]}"
do
        curr_work=$WORK_DIR"/"$ent
        cd "$curr_work"
	pwd=$(pwd)
	echo "Current dir: "$pwd
        # check the backup file exists
        file_list=$(ls -l |grep "$BU_DATE" |awk '{print $9}')
        chk=$(echo $file_list |wc -l)
        if [ $chk -gt 0 ]
        then
		echo "Checking each backup files in: "$pwd
                # call "comp" with backup files in each directory
                while IFS="-" read -ra filename
                do
                        if [ ! -z "${filename[0]}" ]
                        then
				echo "Find files with "${filename[0]}"-"
                                comp "${filename[0]}"-
                        fi
                done <<< "$file_list"
        else
                msg=$msg" WARN: No backup files of \```$curr_work\``` at $BU_DATE\r\n"
        fi
        cd "$WORK_DIR"
done

chk=$(echo $msg)
if [ -z $chk ]
then
        msg='All backup cronjobs are confirmed'
fi

#curl -X POST -H 'Content-type: application/json' --data "{'text':'$msg'}" $WEB_HOOK
wget -q -O /dev/null -S --header="Content-type: application/json" --post-data "{'text':'$msg'}" $WEB_HOOK
echo "Slack webhook sent"
