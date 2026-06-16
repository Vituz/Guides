## Configurazione cache centralizzata

### Creazione della cartella condivisa

```bash
mkdir -p /opt/npm-cache
chmod 755 /opt/npm-cache
```

### Configurazione npm su ogni singolo progetto

Non essendo possibile configurare globalmente npm dal momento che ogni istanza usa il suo Utente e Contesto è necessario salvare un gile in ogni istanza.

```bash
# /var/www/vhosts/cliente-X/httpdocs/.npmrc
cache=/opt/npm-cache
```

Così indipendentemente da quale utente lancia npm install, la cache usata è sempre /opt/npm-cache.


### Script per la propagazione su ogni istanza

```bash
#!/bin/bash
VHOSTS="/var/www/vhosts"
CACHE_DIR="/opt/npm-cache"

# Crea la cartella cache con permessi aperti
mkdir -p "$CACHE_DIR"
chmod 777 "$CACHE_DIR"

for dir in "$VHOSTS"/*/httpdocs; do
    if [ -f "$dir/package.json" ]; then
        echo "cache=$CACHE_DIR" > "$dir/.npmrc"
        echo "✓ Configurato: $dir"
    fi
done
```

# -----------

## Procedura configurazione Globale

### Configurazione Globale npm

```bash
npm config set cache /opt/npm-cache --global
```

### Verifica

```bash
npm config get cache
# → /opt/npm-cache
```

Da questo momento ogni npm install su qualsiasi istanza popola e legge dalla stessa cache.


