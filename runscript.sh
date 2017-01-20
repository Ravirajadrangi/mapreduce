#!/bin/bash
echo 'setup...'
sudo yum install python34 python34-pip gcc python34-devel -y
sudo python3 -m pip install requests
echo 'setup complete'

echo 'initiating...'
python3 scraper.py 
tar czf output.tar.gz output.csv fails.csv nohup.out
python3 -m http.server 8000 &

