# Plan détaillé – Installation, Migration & sauvegarde **n8n → Supabase Postgres** 

 Ubuntu 22.04 (VPS) • Coolify 4 • Docker Compose v2  • DNS avec sous-domaine prêt : n8n/supabase • WIN SCP pour vérifier les dossiers et placer des documents en cas de redéploiements

# Précision supplémentaire à venir

Plan de route initial Chat GPT o3, modifié pour être adapté au stack. Avec des captures d'écrans et un détail de votre stack il pourras adapter cette feuille de route. 
Donner-lui ce qui est déja existant et ou vous êtes arrivés, un screen de ce qui bug. 
---

## Légende

| Symbole | Signification |
|---------|---------------|
| [ ]     | tâche à faire |
| ➜       | tâche en cours |
| [x]     | tâche terminée |

Toutes les commandes sont à exécuter **depuis l’hôte** (root) sauf mention contraire.  
Remplace chaque `<placeholder>` par ta valeur personnelle.

---

## 0 • Récapitulatif (ce qui est déjà fait)

|Supabase déja installer dans un service indépendant (dans le même projet) bien coché 'Connect to predifined Network' |
| noté les noms des contenaires (coolify fait des noms à rallonge) sur un .txt

---


## 1 • Préparation Supabase

1.0 Supabase installé par stack coolify  et reachable par un sous-domaine. 
'''bash 
docker ps -a (pour trouver l'uuid du contenaire Supabase DB)

 1.1  Se connecter en psql à postgres :

```sql
create database n8n;
create user n8n password '<mot‑de‑passe‑fort>'; 
grant all privileges on database n8n to n8n;
```


 1.2 Aucune table à créer : n8n initialise le schéma `public` au premier démarrage. 


## 2 • Pré‑requis système

2.1  Générer (ou localiser) une clé d’encryptage **persistante** :

```bash
openssl rand -hex 32   # note le résultat → N8N_ENCRYPTION_KEY
```

2.2  Récupérer les informations Supabase :

| Variable | Exemple |
|----------|---------|
| Host     | `<contenairesupabase-db>` |
| Port     | `5432` |
| Database | `n8n` |
| User     | `n8n` |
| Password | `<mot‑de‑passe‑fort>` |


---

## 3 • Préparation des variable env dans l'UI Coolify 

3.1 
 - DB_POSTGRESDB_DATABASE : n8n
 - DB_POSTGRESDB_HOST : `<contenairesupabase-db>`
 - DB_POSTGRESDB_PASSWORD : `<mot‑de‑passe‑fort>`
 - DB_POSTGRESDB_USER : n8n
 - N8N_EDITOR_BASE_URL : https://<ex.domaine.com> // Pareil pour WEBHOOK_URL : https://<ex.domaine.com>
 - N8N_ENCRYPTION_KEY : # note le résultat → N8N_ENCRYPTION_KEY ici 
 - N8N_HOST : <ex.domaine.com>

---

## 4 • Préparation des volumes hôte

```bash
# Base SQLite (optionnel si tu ne la gardes pas) et fichiers de config
sudo mkdir -p /srv/n8n_data

# Exports JSON + dumps SQL
sudo mkdir -p /srv/n8n_backup/{workflows,credentials,pgdump}

# Volume partagé existant
sudo mkdir -p /srv/shared

# Droits pour l’utilisateur ‘node’ (uid 1000 dans l’image) et 0:0 (uid build)

sudo chown -R 1000:1000 /srv/n8n_data /srv/n8n_backup #n8n
sudo chown -R 1000:1000 /srv/shared && sudo chown -R 0:0 # u et g dans converter (peux être adaté à chaque contenaire "Build Dockerfile")
sudo find /srv/shared -type f -name "*.sh" -exec chmod u+x {} + # si tu as des script python


```

---

## 5 Mise à jour du `docker-compose.yml`

## 6 • Déploiement initial & import

| Sous‑étape | Commande | État |
|------------|----------|------|
| 6.1 Relancer depuis coolify (redeploy) /!\ bien cocher Connect to predifined networks pour 
| 6.2  Vérifier l’UI (https://<ex.domaine.com>) | Workflows, credentials, utilisateur présents ? | [ ] |
| 6.3  **Si tout est OK ->** remonter `n8n` avec `/backup` en **lecture‑écriture** (`:rw`) afin que le side‑car puisse écrire. |  |  |

---

## 7 • Sauvegarde continue

➜ 7.1  Conteneur **n8n-backup** actif :  
 • Exports JSON toutes les 5 min  
 • `pg_dump` complet toutes les 5 min (ajuste la fréquence si besoin).

[ ] 7.2  Mettre en place une rotation / purge (cron hôte ou job n8n) : # garder les 2/3 derniers backups pas de supression hative ou alors suppression 

```bash
find /srv/n8n_backup/pgdump -type f -mtime +30 -delete
```

[ ] 7.3  Optionnel : synchroniser `/srv/n8n_backup` vers un stockage off‑site (S3, Backblaze, rclone…). # possibilités dans le Duplicati Umbrel ? [ ] à essayer

## 8 • Points d’amélioration futurs (roadmap)
* Passage à **n8n scaling multi‑runner** (variables `QUEUE_MODE=redis`, etc.)  
* Ajout d’un **Redis** managé Supabase pour gérer les queues.  
* Intégration **CI/CD GitHub Actions** : push → test → redeploy Coolify.  
* Chiffrement At‑Rest : Supabase ≥ PostgreSQL 13 chiffre par défaut le disque, vérifier la compliance.

---
