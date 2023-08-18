#!/bin/bash

#pip3 install -r requirements.txt

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")
echo $SCRIPTPATH

sudo rm -f /lib/systemd/system/rhasspy.skill.timer.service
touch /lib/systemd/system/rhasspy.skill.timer.service
:> /lib/systemd/system/rhasspy.skill.timer.service

echo "
[Unit]
Description=Rhasspy timer Skill
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $SCRIPTPATH/action-timer.py
WorkingDirectory=$SCRIPTPATH
Restart=on-abort

[Install]
WantedBy=multi-user.target

  " >>  /lib/systemd/system/rhasspy.skill.timer.service


chmod +x action-timer.py


sudo sudo chmod 644 /lib/systemd/system/rhasspy.skill.timer.service
sudo systemctl stop rhasspy.skill.timer.service
sudo systemctl daemon-reload
sudo systemctl enable rhasspy.skill.timer.service
sudo systemctl start rhasspy.skill.timer.service
#sudo reboot
