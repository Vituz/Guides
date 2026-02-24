Controllo veloce
```bash
lsblk

```


Se NON è 1 Tb (o il valore assegnato) fai rescan:
```bash
echo 1 | sudo tee /sys/class/block/sda/device/rescan
sudo partprobe
lsblk
```

Estendi la partizione /dev/sda3 o nell’sda root
```bash
sudo dnf -y install cloud-utils-growpart
```

Poi:
```bash
sudo growpart /dev/sda 3
sudo partprobe
lsblk
```

A questo punto sda3 deve risultare molto più grande (quasi 1TB, tolto sda1+sda2).

Estendi il Physical Volume:
```bash
sudo pvresize /dev/sda3
```

Controllo:
```bash
sudo pvs
sudo vgs
```

Dai lo spazio a root (consigliato) e ridimensiona XFS
```bash
sudo lvextend -l +100%FREE -r /dev/almalinux/root
```

Verifica finale:
```bash
df -hT /
sudo lvs
```