## Installazione di Nginx RTMP
Nginx RTMP serve a decodificare il video ricevuto da FlightHub 2 per renderlo visibile su una pagina Html
Se Nginx è già presente, scaricare i file e i pacchetti nella cartella /home/

```bash
sudo dnf install gcc-c++ pcre-devel zlib-devel openssl-devel

wget http://nginx.org/download/nginx-1.20.1.tar.gz
wget https://github.com/arut/nginx-rtmp-module/archive/master.zip

tar -zxvf nginx-1.20.1.tar.gz
unzip master.zip
```

#### Compilazione Nginx + RTMP
Dopo aver completato tutto il processo di installazione spostarsi nella cartella di Nginx
```bash
cd nginx-1.20.1
./configure --prefix=/usr/share/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib64/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --http-client-body-temp-path=/var/lib/nginx/tmp/client_body --http-proxy-temp-path=/var/lib/nginx/tmp/proxy --http-fastcgi-temp-path=/var/lib/nginx/tmp/fastcgi --http-uwsgi-temp-path=/var/lib/nginx/tmp/uwsgi --http-scgi-temp-path=/var/lib/nginx/tmp/scgi --pid-path=/run/nginx.pid --lock-path=/run/lock/subsys/nginx --user=nginx --group=nginx --with-compat --with-debug --with-file-aio --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_degradation_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_image_filter_module=dynamic --with-http_mp4_module --with-http_perl_module=dynamic --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-http_xslt_module=dynamic --with-mail=dynamic --with-mail_ssl_module --with-pcre --with-pcre-jit --with-stream=dynamic --with-stream_ssl_module --with-stream_ssl_preread_module --with-threads --with-cc-opt='-O2 -flto=auto -ffat-lto-objects -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -fstack-protector-strong -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -march=x86-64-v2 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection' --with-ld-opt='-Wl,-z,relro -Wl,--as-needed -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -Wl,-E' --add-module=../nginx-rtmp-module-master

make
sudo make install
```

Il processo ./configure potrebbe dare problemi per la mancanza di alcuni pacchetti, ad ogni esecuzione fare riferimento al pacchetto mancante da installare. Successivamente rilanciare il processo ./configure. Ripetere il processo per ogni pacchetto mancante.

Finito il ./configure procedere all’installazione con make e sudo make install.

#### Errore del make install
Se si verificano errori durante questo processo potrebbe essere necessatio eliminare il -Werror dal file di nginx.

```bash
cd objs
sudo nano Makefile
```
All’interno del file cercare la variabile CFGLASS ed eliminare -Werror. La variabile dovrebbe essere ad inizio file.
```bash
CFLAGS = -pipe -O -W -Wall -Wpointer-arith -Werror ... ecc
```
Salvare il file ed effettuare di nuovo make - sudo make install

#### Modificare il file di Nginx
Se tutto è andato a buon fine, bisogna modificare i file di Nginx.
```bash
sudo nano /etc/nginx/nginx.conf
```
Aggiungere il seguente codice prima del blocco http
```bash
rtmp {
    server {
        listen 1935;
        chunk_size 4096;

        application live {
            live on;
            record off;
            hls on;
            hls_path /var/www/html/hls;
            hls_fragment 3s;
        }
    }
}
```
listen 1935: Ascolta le connessioni in arrivo sulla porta RTMP standard.

application live: Definisce un'applicazione di streaming chiamata live.

live on: Abilita lo streaming dal vivo.

hls on: Abilita lo streaming HLS.

hls_path /var/www/html/hls: Specifica la directory in cui Nginx salverà i segmenti video HLS. Assicurati che il percorso esista e che Nginx abbia i permessi di scrittura.

hls_fragment 3s: Suddivide il flusso in segmenti di 3 secondi.


Verificare che il file sia correttamente formattato
```bash
sudo nginx -t
```
Riavviare Nginx
```bash
sudo systemctl restart nginx
```

Se tutto funziona correttamente, nel file che abbiamo appena modificato è necessario configurare gli URL per il salvataggio temporaneo dei video da riprodurre.

Nel blocco server aggiungere il seguente codice:
```bash
server {
    listen 80;
    listen [::]:80;
    server_name _;
    root /usr/share/nginx/html;

    # ... altre configurazioni del tuo sito ...
    # Blocco da aggiungere
    location /hls {
        types {
            application/vnd.apple.mpegurl m3u8;
            video/mp2t ts;
        }
        root /var/www/html/;
        add_header Cache-Control no-cache;
    }
    # fine blocco

    # ...
}
```
location /hls: Definisce un punto di accesso web per il tuo streaming.

root /var/www/html/: Specifica il percorso radice per i file HLS.

#### Prima di poter riavviare Nginx è necessario verificare che il path /var/www/html/hls esista, altrimenti è necessario crearlo

Ora è possibile includere i video nel codice html
```html
<video id="drone-video" class="video-js vjs-default-skin" controls preload="auto" width="640" height="360" data-setup='{}'>
    <source src="http://tuo.server.com/hls/drone1_main_camera.m3u8" type="application/x-mpegURL">
</video>
```


## Estratto da Gemini:
Abbiamo configurato Nginx per gestire più video. La configurazione che ti ho fornito con il blocco rtmp e application live è già pronta per questo scopo.

Come funziona
Il blocco application live agisce come un'unica "porta" per tutti i flussi video. Nginx riconosce i diversi flussi in base alla chiave di flusso (stream_key) che invierai da FlightHub 2.

In questo modo, non devi aggiungere un nuovo blocco application per ogni drone. Puoi inviare un numero illimitato di flussi, a condizione che ciascuno abbia una chiave di flusso univoca.

Esempi di URL
Come abbiamo visto, i tuoi URL di streaming RTMP per FlightHub 2 saranno:

Drone A: rtmp://[tuo.server.com]:1935/live/droneA_main_cam

Drone B: rtmp://[tuo.server.com]:1935/live/droneB_fpv_cam

E gli URL HLS per il tuo sito web saranno:

Drone A: http://[tuo.server.com]/hls/droneA_main_cam.m3u8

Drone B: http://[tuo.server.com]/hls/droneB_fpv_cam.m3u8

Quando un drone inizia a trasmettere, Nginx creerà automaticamente un nuovo flusso HLS nella directory /var/www/html/hls con il nome della chiave di flusso. Il tuo sito web potrà quindi riprodurre quel flusso.