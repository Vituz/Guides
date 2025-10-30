## CREAZIONE FILE DISABILITAZIONE FIREWALLD ALL’AVVIO

### Creazione file:
```bash
/usr/local/bin/disable-firewall.sh
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
chmod +x /usr/local/bin/disable-firewall.sh
```

### Crea il file:
```bash
/etc/systemd/system/disable-firewall.service
```

```ini
[Unit]
Description=Disabilita il firewall dopo 30 secondi dall'avvio
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
systemctl enable disable-firewall.service
```