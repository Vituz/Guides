# Eseguire correttamente un Merge

### Posizionarsi sul branch sul quale si vuole mergare le modifiche di altri branch
```shell
git checkout nome_branch
```

### Aggiornare il branch locale dal quale prendere le modifiche
il primo "nome_branch" si riferisce al nome del branch remoto, il secondo "nome_branch" si riferisce al nome del branch locale (di solito coincidono).
```shell
git fetch origin nome_branch:nome_branch
```

### Eseguire il merge
```shell
git merge origin/nome_branch
```

### Risolvere eventuali conflitti e salvare i file. Successivamente pushare tutte le nuove modifiche sul proprio branch remoto
```shell
git add .
git commit -m "Commento"
git push
```

