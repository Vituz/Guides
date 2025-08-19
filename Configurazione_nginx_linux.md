# Dopo aver installato nginx creare il file di gestione
```bash
sudo nano /etc/nginx/conf_d/nome_file.conf
```

In questo caso sono stati realizzati due endpoint di tipo location per poter gestire due istnaze separate dell’app,
una per Dryad ed una per AgroForeSight
```nginx
  GNU nano 5.6.1                                                                                            
  etc/nginx/conf.d/dryad.conf                                                                                                      
server {
    listen 80;
    listen 443;
    server_name 10.100.10.68;

    location /dryad/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header X-Site-Prefix dryad;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_redirect off;
    }

    location /agroforesight/ {
        proxy_pass http://127.0.0.1:8001/;
        proxy_set_header X-Site-Prefix agroforesight;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_redirect off;
    }

    location /dryad/static/ {
        alias /home/v.battaglia/agf-dryad/agriforesight-frontend/dryad/staticfiles/;
    }

location /agroforesight/static/ {
        alias /home/v.battaglia/agriforesight-frontend/dryad/staticfiles/;
}
}
```