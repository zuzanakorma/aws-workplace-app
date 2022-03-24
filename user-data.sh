#!/bin/bash

# This script is to be used with AWS EC2 user-data
# where the commands are run as root user, reason
# for not using sudo and also changing directories
# and files ownership to ec2-user (this demo uses AWS Linux)

yum install -y git

cd /home/ec2-user/
git clone https://github.com/zuzanakorma/workplace-app-aws.git

cd workplace-app-aws/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
deactivate

# ====
# This is to address the ownsership of files/directories when
# using AWS EC2 user-data. We want to make sure to set the right
# owner for our application
cd ..
chown -R ec2-user:ec2-user workplace-app-aws/

# create multiline file for workplaceapp.service
tee /etc/systemd/system/workplaceapp.service <<EOF
[Unit]
Description=Gunicorn instance for workplace app
After=network.target
[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/workplace-app-aws
ExecStart=/home/ec2-user/workplace-app-aws/venv/bin/gunicorn -b localhost:8080 run:app
Restart=always
[Install]
WantedBy=multi-user.target
EOF

# Every time you create a new service file in Systemd, you have to reload
# the daemon to detect the file
systemctl daemon-reload
systemctl start workplaceapp
systemctl enable workplaceapp
systemctl status workplaceapp


amazon-linux-extras install -y nginx1
# create multiline file for nginx configuration
tee /etc/nginx/conf.d/workplaceapp.conf <<EOF
upstream workplaceapp {
  server 127.0.0.1:8080;
}
EOF

tee /etc/nginx/default.d/workplaceapp.conf <<EOF
location / {
  # pass requests to the Flask host
  proxy_pass http://workplaceapp;
}
EOF

systemctl start nginx
systemctl enable nginx
systemctl status nginx
