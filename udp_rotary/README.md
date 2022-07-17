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


# i2c

configure `/boot/uEnv.txt` in this way:

```bash
verbosity=7
overlay_prefix=rockchip
rootfstype=ext4
fdtfile=rockchip/rk3308-rock-pi-s.dtb
console=ttyS0,1500000n8
overlays=rk3308-uart0 rk3308-i2c3
rootuuid=2a975457-7408-4fda-bd37-22b8d2df5b6f
initrdsize=0x5c9c89
kernelversion=4.4.143-67-rockchip-g01bbbc5d1312
initrdimg=initrd.img-4.4.143-67-rockchip-g01bbbc5d1312
kernelimg=vmlinuz-4.4.143-67-rockchip-g01bbbc5d1312
```

and connect i2c device to theese pins:


| ------- | ----- |
| rockpis | dev   |
| ------- | ----- |
| 11      | 2 DIO |
| 13      | 1 CLK |