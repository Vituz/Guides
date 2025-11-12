### Creazione SSH
#### Creazione di una chiave ssh generale per abilitare una vm su gitlab

```bash
ssh-keygen -t ed25519 -C "plesk@guild-dev"
```

Leggiamo la chiave per poterla copiare nel profilo gitlab
```bash
cat /root/.ssh/id_ed25519.pub 
```

#### Creare un file di configurazione globale per tutti gli utenti
Crearlo nel seguente percorso:
```bash
nano /etc/ssh/ssh_config.d/gitlab.conf
```
con il seguente contenuto:
```sh
Host gitlab.com
    HostName gitlab.com
    User git
    IdentityFile /etc/ssh/gitlab-shared/id_ed25519
    IdentitiesOnly yes
```

#### Spostare la chiave privata in un percorso accessibile a tutti gli utenti ma in sola lettura (esempio /etc/ssh/plesk-shared/id_ed25519)
```bash
sudo mkdir -p /etc/ssh/gitlab-shared
sudo cp /root/.ssh/id_ed25519.pub /etc/ssh/gitlab-shared/
sudo cp /root/.ssh/id_ed25519 /etc/ssh/gitlab-shared/
sudo chown root:root /etc/ssh/gitlab-shared/id_ed25519
sudo chmod 644 /etc/ssh/gitlab-shared/id_ed25519
sudo chmod 644 /etc/ssh/gitlab-shared/id_ed25519.pub
sudo chmod 644 /etc/ssh/ssh_config.d/gitlab.conf
```

Verificare se altri utenti hanno accesso
```bash
sudo -u v.battaglia ssh -T git@gitlab.com
```