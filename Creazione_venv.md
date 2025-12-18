## Creazione file requirements.txt
Il file requirements.txt viene generato sulla base di tutti i moduli installati nel software che stiamo scrivendo. È molto utile quando dobbiamo cambiare macchina o creare un nuovo progetto con gli stessi moduli, senza doverli installare singolarmente uno per uno.
Il nome requirements.txt è un convenzione.

```shell
python -m pip freeze > requitements.txt
```
Questo comando genererà il file nella cartella in cui ci troviamo, generalmente nella root del progetto.

Output file di esempio:
```txt
arrow==1.3.0
asgiref==3.8.1
binaryornot==0.4.4
certifi==2025.1.31
chardet==5.2.0
charset-normalizer==3.4.1
click==8.1.8
colorama==0.4.6
cookiecutter==2.6.0
Django==5.1.5
django-tailwind==4.0.1
```

## Creazione di un Virtual Environment
Consente di creare un Virtual Environment dove installare tutti i moduli necessari al funzionamento del software senza installarli sulla macchina. Questo consente di non avere problemi di versione dei moduli tra i vari Progetti

```shell
python -m venv 'nome_venv'
```

### Attivazione del venv
Spostarsi nella cartella contenente il venv

#### Win
```shell
'nome_venv'/Scripts/activate
```
#### Linux
```bash
source 'nome_venv'/bin/activate
```

### Installazione del requirements.txt
Il file requirements.txt contiene tutti moduli importati nel progetto

```shell
python -m pip install -r requirements.txt
```

### Nel caso in cui il comando python non funzionasse su linux/mac provare con python3