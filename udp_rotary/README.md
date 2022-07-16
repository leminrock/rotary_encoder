# services

copy service files in `/etc/systemd/system` folder:

```bash
sudo cp rotary_client.service /etc/systemd/system/.
sudo cp rotary_server.service /etc/systemd/system/.
```

then execute these command:

```bash
sudo systemctl enable rotary_client.service
sudo systemctl enable rotary_server.service
```

reboot.