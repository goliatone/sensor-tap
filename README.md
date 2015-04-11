# sensor-tap
Collect grovepi sensor data


```bash
chmod 755 sensor_collector.py
sudo cp sensor-tap /etc/init.d
chmod 755 /etc/init.d/sensor-tap
sudo update-rc.d sensor-tap defaults
```

### TODO:
- Add logger
- Make for realz!

http://linuxcommand.org/man_pages/logrotate8.html

Check out:
https://github.com/taka-wang/py-beacon

TODO:
- Make movement detector realtime, separated track.
- Use mqtt or similar queue to collect sensor data