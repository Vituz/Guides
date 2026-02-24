## Creazione file whitelist del processo OAuth Google

```bash
sudo nano /etc/httpd/conf.d/modsecurity_custom.conf
```

#### Nel file copiamo il testo seguente
```txt
# Disabilita regola 210580 per OAuth callbacks (falso positivo su .profile)
<LocationMatch "^/oauth/(google|microsoft)/callback">
    SecRuleRemoveById 210580
</LocationMatch>
```

#### Poi riavviamo il processo httpd o apache2

```bash
sudo systemctl restart httpd
```

oppure

```bash
sudo systemctl restart apache2
```