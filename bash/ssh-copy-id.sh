# expect example
#!/bin/bash
remote=$1
pw=$2

#spawn ssh-copy-id -o StrictHostKeyChecking=no -i /var/lib/geofront/id_rsa.pub $remote
expect << EOF
spawn ssh-copy-id -i /PATH_TO_HOME/.ssh/id_rsa.pub $remote
expect {
    "(yes/no)?" { send "yes\n"; exp_continue }
    "password:" { send "$pw\n"; exp_continue }
    eof
}
