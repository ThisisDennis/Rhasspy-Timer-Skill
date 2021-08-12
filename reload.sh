#!/bin/bash
sudo systemctl stop rhasspy.skill.timer.service
sudo systemctl daemon-reload
sudo systemctl start rhasspy.skill.timer.service