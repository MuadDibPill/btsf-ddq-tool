# BTSF DDQ Automation — Guide de déploiement

Trois façons de lancer l'interface, de la plus simple à la plus avancée.

---

## Structure complète des fichiers

```
projet/
├── ddq_app/                  ← outil Python (déjà fourni)
│   ├── main.py
│   ├── config.py
│   └── core/
│       ├── ingestion.py
│       ├── signals.py
│       ├── questions.py
│       ├── generator.py
│       ├── writer.py
│       ├── drive.py
│       └── schema.py
│
└── ddq_web/                  ← interfaces web (ce dossier)
    ├── app.py                ← interface Flask
    ├── streamlit_app.py      ← interface Streamlit
    ├── requirements.txt      ← dépendances
    ├── render.yaml           ← config déploiement Render
    ├── Procfile              ← fallback Render
    ├── templates/
    │   └── index.html        ← page HTML de l'interface Flask
    └── README.md             ← ce fichier
```

---

## Option A — Flask (usage local ou réseau interne)

### Installation

```powershell
cd ddq_web
pip install flask gunicorn
pip install anthropic pdfplumber docx2txt python-docx openpyxl
```

### Lancement

```powershell
python app.py
```

Ouvre le navigateur sur **http://localhost:5000**

### Partager avec l'équipe (réseau local)

Si toute l'équipe est sur le même réseau Wi-Fi ou VPN :

```powershell
python app.py
```

Les collègues accèdent à l'URL :
**http://TON-IP-LOCAL:5000**

Pour trouver ton IP local sur Windows :
```powershell
ipconfig
```
Chercher "Adresse IPv4" (exemple : 192.168.1.45)

---

## Option B — Streamlit (plus simple, usage local ou cloud)

### Installation

```powershell
pip install streamlit
pip install anthropic pdfplumber docx2txt python-docx openpyxl
```

### Lancement

```powershell
cd ddq_web
streamlit run streamlit_app.py
```

Ouvre automatiquement **http://localhost:8501**

### Avantages Streamlit vs Flask

| | Flask | Streamlit |
|---|---|---|
| Setup | Manuel | Automatique |
| Interface | Custom HTML | Composants prêts |
| Partage réseau | Manuel | `--server.address 0.0.0.0` |
| Déploiement cloud | Gunicorn + Render | Streamlit Cloud (gratuit) |

---

## Option C — Render (déploiement cloud, accès depuis n'importe où)

Render héberge l'application sur un serveur cloud accessible depuis n'importe quel navigateur, sans avoir besoin d'un PC allumé en permanence.

### Étape 1 — Préparer le repo GitHub

Créer un compte GitHub (github.com) si pas encore fait.

Créer un nouveau repository et y uploader tous les fichiers :
```
ddq_app/     (dossier complet)
ddq_web/     (dossier complet)
```

### Étape 2 — Déployer sur Render

1. Aller sur **render.com** et créer un compte (gratuit)
2. Cliquer sur **New** → **Blueprint**
3. Connecter le compte GitHub et sélectionner le repo
4. Render détecte automatiquement `render.yaml` et crée les deux services
5. Dans le dashboard Render, pour chaque service :
   - Aller dans **Environment**
   - Ajouter la variable `ANTHROPIC_API_KEY` = `sk-ant-ta-clé`
6. Cliquer sur **Deploy**

Render génère une URL publique du type :
- Flask :     `https://btsf-ddq-flask.onrender.com`
- Streamlit : `https://btsf-ddq-streamlit.onrender.com`

L'équipe accède à cette URL depuis n'importe où.

### Coûts Render

| Plan | RAM | Prix | Usage recommandé |
|---|---|---|---|
| Free | 512 MB | 0 $/mois | Test uniquement (s'endort après 15 min) |
| Starter | 512 MB | ~7 $/mois | Usage régulier équipe |
| Standard | 2 GB | ~25 $/mois | Gros volumes, data rooms larges |

Pour un usage BTSF, le plan **Starter** est suffisant.

### Alternative gratuite — Streamlit Cloud

Pour Streamlit uniquement, Streamlit Community Cloud est 100% gratuit :

1. Aller sur **share.streamlit.io**
2. Connecter GitHub
3. Sélectionner le repo et le fichier `ddq_web/streamlit_app.py`
4. Ajouter `ANTHROPIC_API_KEY` dans les secrets
5. Déployer

URL publique du type : `https://ton-app.streamlit.app`

---

## Variables d'environnement requises

| Variable | Description | Où la configurer |
|---|---|---|
| `ANTHROPIC_API_KEY` | Clé API Claude | Render dashboard / saisie dans l'interface |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Credentials Google Drive | Render dashboard (optionnel) |

---

## Conseils sécurité

- Ne jamais committer la clé API dans le code ou sur GitHub
- Sur Render, toujours configurer `ANTHROPIC_API_KEY` via le dashboard Environment, jamais dans le code
- Les fichiers uploadés sont temporaires et supprimés après chaque run
- L'interface Flask ne stocke pas les clés API entre les sessions

---

## Résolution de problèmes courants

**`ModuleNotFoundError: No module named 'core'`**
→ Vérifier que `ddq_app/` et `ddq_web/` sont au même niveau dans le repo

**Timeout sur Render**
→ Passer au plan Standard (plus de RAM) ou réduire la data room

**`ANTHROPIC_API_KEY not set`**
→ Ajouter la variable dans Render Dashboard → Environment → Add variable

**Upload trop lent**
→ Normal pour des PDF lourds — la limite est 100 MB par upload
