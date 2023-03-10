#sudo chown root:root IC7300_Time_Sync.service
#sudo cp IC7300_Time_Sync.service /lib/systemd/system/.

#sudo systemctl daemon-reload 
#sudo systemctl enable IC7300_Time_Sync.service
#sudo systemctl start IC7300_Time_Sync
#sudo systemctl status IC7300_Time_Sync

#echo Reboot in 10 secs
#sleep 10 && sudo reboot 