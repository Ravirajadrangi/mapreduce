#!/bin/bash

read host

#command="tar xzf ~/src.tar.gz && cd ~/src/ && chmod +x runscript.sh && (nohup ./runscript.sh > /dev/null 2>&1 &)"

command="(tar xzf ~/src.tar.gz; cd ~/src/; chmod +x runscript.sh; ./runscript.sh > a.txt && touch ok.txt) &>/dev/null &"

echo "..."

ssh -i cluster.pem -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no" ec2-user@$host "$command"

