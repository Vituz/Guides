# --------------------------------------------------
### Vedere chi sta occupando la porta
```bash
sudo netstat -tulpn | grep :8000
```

### Killa il processo che occupa la porta
```bash
sudo kill -9 <codice processo>
```

### da terminale della vm verificare che gunicorn risponda correttamente
```bash
curl -I http://127.0.0.1:8000/
```

### da terminale della vm verificare che il sito risponda
```bash
curl -I http://127.0.0.1/dryad/
```

### Startare gunicorn da dentro la cartella del progetto
```bash
gunicorn --bind 127.0.0.1:8000 dryad.wsgi
```

### Dopo aver verificato che il file dryad.conf dentro la dir di nginx/conf.d sia corretto riavviare nginx
```bash
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status nginx
```

### Se riceviamo l’errore 502 bad gateway potrebbe essere che nginx non abbia i permessi per connettersi, vericarli con:
```bash
sudo tail -n 20 /var/log/nginx/error.log
```

### Abilitare i permessi di connessione per nginx
```bash
sudo setsebool -P httpd_can_network_connect on
```

### Usando pawershell usare il comando seguente per verificare la connessione
```bash
Invoke-WebRequest -Uri http://10.100.10.68/dryad/ -Method Head
```

### Siccome nginx usa la porta 80, verificare che funzioni
```bash
sudo netstat -tulpn | grep :80
```

### Verificare dal tuo pc che la porta sia accessibile
```bash
Test-NetConnection -ComputerName 10.100.10.68 -Port 80
```

### Applicare il contesto corretto ai file statici per consentire a nginx di leggerli
```bash
sudo chcon -R -t httpd_sys_content_t /home/v.battaglia/agriforesight-frontend/dryad/staticfiles
```

### poi riavviare nginx
```bash
sudo systemctl restart nginx
```

### verificare che venga restituito 200 invece di forbidden
```bash
curl -I http://10.100.10.68/static/home/login_page.css
```
## ------------------------------------
### verificare permessi di una cartella
```bash
ls -ld percorso/cartella

drwxrwxr-x. 7 v.battaglia nginx 4096 May 21 12:07 home/v.battaglia/agriforesight-frontend/dryad/staticfiles/
```

Interpretazione:

d: è una directory

rwx: utente (owner) può leggere, scrivere, ed eseguire (entrare nella cartella)

r-x: gruppo può leggere ed entrare

r--: altri possono solo leggere (ma non entrare senza x)

## ------------------------------------

### Cambiare il proprietario di una directory ma rende troppo aperti i permessi assegnando i 777
```bash
sudo chown -R v.battaglia:nginx /home/v.battaglia/agriforesight-frontend/dryad/staticfiles/
```

### Assegnamo i permessi 775 che sono più restrittivi
```bash
chmod -R 775 /home/v.battaglia/agriforesight-frontend/dryad/staticfiles/
```

### Aggiungere l’user corrente al gruppo del software che ha tutti i permessi sulla directory per fargli avere gli stessi permessi
```bash
sudo chmod -R g+w /home/v.battaglia/agriforesight-frontend/dryad/staticfiles/
```

### Questo comando permette a chiunque di leggere e scrivere sulla cartella (poco consigliato)
```bash
sudo chmod -R a+rwX /home/v.battaglia/agriforesight-frontend/dryad/staticfiles/
```
