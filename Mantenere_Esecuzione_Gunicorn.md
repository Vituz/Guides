### Creare il file di gunicor
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

### Scrivere nel file:
```ini
[Unit]
Description=Gunicorn instance on port 8000 (o quello che deve fare il servizio)
After=network.target

[Service]
User=tuo_utente
Group=www-data (scegli il gruppo al quale assegnare la visione del file)
WorkingDirecotry=/percorso/app
ExecStart=/percorso/app/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 app.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Attivazione del servizio
```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn (guinoirn è il nome del file .service che abbiamo creato)
sudo systemctl enable gunicorn (guinoirn è il nome del file .service che abbiamo creato)
```

### Verificare che il servizio sia attivo
```bash
sudo systemctl status gunicorn (nome del file .service)
```


### Se si ottengono errori sui permessi eseguire i seguenti passaggi:
```bash
ls -l /percorso/app/venv/bin/gunicorn
```
### Risposta:
```bash
-rwxr-xr-x 1 v.battaglia v.battaglia ... gunicorn
```
Verificare che sia presente l’ultima x che rappresenta la lettura, altrimenti modifichiamo il permesso
```bash
chmod +x /percorso/app/venv/bin/gunicorn
```
### Verifichiamo i permessi sulle cartelle:
```bash
namei -l /percorso/app/venv/bin/guniorn
```
Verificare che ogni directory del percorso abbia almeno --x per l’esecuzione del servizio (es. v.battaglia)
Se si riceve ancora Permission denied, il problema potrebbe essere SELinux (se attivo)

```bash
sestatus

sudo setenforce 0
```