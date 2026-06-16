## Trova l'ID del dominio Plesk:

```bash
mysql -uadmin -p`cat /etc/psa/.psa.shadow` psa -e "SELECT id, name FROM domains WHERE name='tuodominio.it';"
```

## Entra nel database del Laravel Toolkit:

```bash
sqlite3 /usr/local/psa/var/modules/laravel/laravel_toolkit.sqlite3
```

## Trova la cartella git associata a quel dominio:

```sql
SELECT * FROM applications WHERE domainId=372;
```

Il campo repositoryPath (nel tuo caso laravel_2c50b3) è il nome della cartella dentro /var/www/vhosts/tuodominio.it/git/ che il Laravel Toolkit sta effettivamente usando.