
### Capire come è fatto
```bash
lsblk -o NAME,SIZE,FSTYPE,TYPE,MOUNTPOINTS
sudo fdisk -l
df -hT
```

Se vedi qualcosa tipo ubuntu--vg-ubuntu--lv o dm-0 sotto a sda3 → probabilmente LVM
Se vedi una partizione tipo /dev/sda2 montata su / senza LVM → partizione “normale”

### Installiamo Growpart se non è già presente
```bash
sudo apt-get update
sudo apt-get install -y cloud-guest-utils
```

### Caso in cui il disco sia LVM
Estendere la partizione LVM
```bash
lsblk -f
sudo lvs
```

Se il PV è su /dev/sda3, estendi quella partizione:
```bash
sudo growpart /dev/sda 3
```

B2) Ridimensionare il PV
```bash
sudo pvresize /dev/sda3
```

B3) Estendere il Logical Volume + filesystem in automatico
Se il filesystem è ext4 (di solito sì su Ubuntu):
```bash
sudo lvextend -l +100%FREE -r /dev/ubuntu-vg/ubuntu-lv
```

-l +100%FREE usa tutto lo spazio libero nel VG
-r ridimensiona anche il filesystem automaticamente

Verifica
```bash
df -hT /
sudo lvs
sudo vgs
```
