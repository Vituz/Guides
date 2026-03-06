## CREAZIONE FILE DISABILITAZIONE FIREWALLD ALL’AVVIO

### Crea il file:
```bash
nano /usr/local/bin/disable-firewalld.sh
```

```ini
#!/bin/bash
# Attende 30 secondi dopo l'avvio
sleep 30
# Disabilita e ferma firewalld
systemctl stop firewalld
systemctl disable firewalld
```

### Poi rendilo eseguibile:

```bash
chmod +x /usr/local/bin/disable-firewalld.sh
```

### Crea il file:
```bash
nano /etc/systemd/system/disable-firewalld.service
```

```ini
[Unit]
Description=Disabilita il firewalld dopo 30 secondi dall'avvio
After=network.target


[Service]
Type=simple
ExecStart=/usr/local/bin/disable-firewall.sh
Restart=no


[Install]
WantedBy=multi-user.target
```

### Abilita il servizio all’avvio

```bash
systemctl daemon-reload
systemctl enable disable-firewalld.service
```


# Rendi masked (impedisce qualsiasi avvio, anche manuale o automatico)
```bash
sudo systemctl mask firewalld
```

# In caso si voglia togliere il masked
```bash
sudo systemctl unmask firewalld
sudo systemctl start firewalld
```