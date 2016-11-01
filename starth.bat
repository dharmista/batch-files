@echo off
echo Username : baba
SET /P pwd=enter password: 
netsh wlan set hostednetwork mode=allow ssid=baba key=%pwd%
netsh wlan start hostednetwork