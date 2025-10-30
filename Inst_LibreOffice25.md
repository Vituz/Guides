## Installazione LibreOffice

Link al file compresso da scaricare:
https://download.documentfoundation.org/libreoffice/stable/25.8.2/rpm/x86_64/LibreOffice_25.8.2_Linux_x86-64_rpm.tar.gz

Verificare che sia la versione più aggiornata o stabile

```bash
wget https://download.documentfoundation.org/libreoffice/stable/25.8.2/rpm/x86_64/LibreOffice_25.8.2_Linux_x86-64_rpm.tar.gz
```

#### Estrarre il contenuto
```bash
tar -xzvf LibreOffice_25.8.2_Linux_x86-64_rpm.tar.gz
```

Verificare se presente la vecchia versione di LibreOffice ed liminarla.
Nelle repo di Alma Linux è presente solo la version 7.1. 
```bash
soffice --version

sudo dnf remove libreoffice
```

Entrare nella cartella decompressa e lanciare l’installazione di tutti i file .rpm
```bash
cd LibreOffice_25.8.2.2_Linux_x86-64_rpm/RPMS

sudo dnf install *.rpm
```

Verificare se è stato installato correttamente
```bash
soffice --version
```

### In caso non venga mostrata la versione fare i seguenti step

Verificare che i pacchetti siano installati
```bash
rpm -qa | grep libreoffice
```

Se non ci sono pacchetti installati rimuovere LibreOffice e installarlo di nuovo

Se i pacchetti sono presenti, cercare la posizione dei binari di LibreOffice e di soffice
```bash
sudo find / -name soffice
```
Esempio di risposta: /opt/libreoffice25.8/program/soffice

Se i file non sono in /usr/bin/, dobbiamo creare un collegamento in questo percorso
```bash
sudo ln -s /opt/libreoffice25.8/program/soffice /usr/bin/soffice
```

#### Verificare la versione.
Se ancora non si riesce a verificare la versione di soffice potrebbe essere necessario installare dei pacchetti aggiuntivi, o libX11 o quelli suggeriti dalla macchina
```bash
sudo dnf install libX11-xcb
```

Se tutto funziona correttamente possiamo eliminare i file scaricati
```bash
sudo rm LibreOffice_25.x.x_Linux_x86-64_rpm.tar.gz

rm -rf LibreOffice_25.x.x_Linux_x86-64_rpm
```


## Extra tip
Si può usare il path completo per verificare la versione
```bash
/opt/libreoffice25.8/program/soffice --version
```

Bisogna aggiungere il percorso al PATH di sistema

```bash
export PATH=$PATH:/opt/libreoffice25.8/program/

source ~/.bash_profile
```
oppure
```bash
export PATH=$PATH:/opt/libreoffice25.8/program/

source ~/.bashrc
```
(alt gr per la tilde su tastiera italiana )