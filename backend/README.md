# 🚀 API Portfolio Django REST Framework

API REST complète pour le portfolio de **Traore Husseni** (Développeur Full Stack).

---

## 📦 INSTALLATION

### 1️⃣ Activer l'environnement virtuel

```powershell
# Windows
cd D:\Projets\Angular\Portfolio\backend
env\Scripts\activate

# Vous devriez voir (env) dans votre terminal
```

### 2️⃣ Installer les dépendances (si pas déjà fait)

```powershell
pip install -r requirements.txt
```

**Dépendances :**
- Django 6.0.1
- djangorestframework 3.16.1
- django-cors-headers 4.9.0
- Pillow 12.1.0

### 3️⃣ Appliquer les migrations (si pas déjà fait)

```powershell
python manage.py migrate
```

### 4️⃣ Créer un superuser (si pas déjà fait)

```powershell
python manage.py createsuperuser

# Ou utiliser le compte déjà créé :
# Username: admin
# Password: admin123
```

### 5️⃣ Lancer le serveur

```powershell
python manage.py runserver
```

Le serveur démarre sur : **http://localhost:8000**

---

## 🌐 ACCÈS

- **API REST** : http://localhost:8000/api/
- **Interface Admin** : http://localhost:8000/admin/ (admin / admin123)
- **API Browsable** : http://localhost:8000/api-auth/

---

## 📡 ENDPOINTS DISPONIBLES

### 🧑 Utilisateurs
- `GET    /api/utilisateurs/` - Liste tous les utilisateurs
- `POST   /api/utilisateurs/` - Créer un utilisateur
- `GET    /api/utilisateurs/{id}/` - Détails d'un utilisateur
- `PUT    /api/utilisateurs/{id}/` - Modifier un utilisateur
- `PATCH  /api/utilisateurs/{id}/` - Modifier partiellement
- `DELETE /api/utilisateurs/{id}/` - Supprimer un utilisateur
- `GET    /api/utilisateurs/{id}/portfolio_complet/` - **Tout en un** (user + projets + expériences + services + réseaux + localisations)

### 💼 Projets
- `GET    /api/projets/` - Liste tous les projets
- `POST   /api/projets/` - Créer un projet
- `GET    /api/projets/{id}/` - Détails d'un projet
- `PUT    /api/projets/{id}/` - Modifier un projet
- `DELETE /api/projets/{id}/` - Supprimer un projet
- `GET    /api/projets/?utilisateur={id}` - Filtrer par utilisateur
- `GET    /api/projets/par-utilisateur/{user_id}/` - Projets d'un utilisateur

### 🎯 Expériences
- `GET    /api/experiences/` - Liste toutes les expériences
- `POST   /api/experiences/` - Créer une expérience
- `GET    /api/experiences/{id}/` - Détails d'une expérience
- `PUT    /api/experiences/{id}/` - Modifier une expérience
- `DELETE /api/experiences/{id}/` - Supprimer une expérience
- `GET    /api/experiences/?utilisateur={id}` - Filtrer par utilisateur
- `GET    /api/experiences/par-utilisateur/{user_id}/` - Expériences d'un utilisateur
- `GET    /api/experiences/en_cours/` - Expériences en cours (sans date_fin)

### 🛠️ Services
- `GET    /api/services/` - Liste tous les services
- `POST   /api/services/` - Créer un service
- `GET    /api/services/{id}/` - Détails d'un service
- `PUT    /api/services/{id}/` - Modifier un service
- `DELETE /api/services/{id}/` - Supprimer un service
- `GET    /api/services/?type={type}` - Filtrer par type
- `GET    /api/services/disponibles/` - Services disponibles

### 📧 Contacts (Prise de contact)
- `GET    /api/contacts/` - Liste tous les messages
- `POST   /api/contacts/` - Créer un message de contact
- `GET    /api/contacts/{id}/` - Détails d'un message
- `PATCH  /api/contacts/{id}/marquer_lu/` - Marquer comme lu
- `DELETE /api/contacts/{id}/` - Supprimer un message
- `GET    /api/contacts/?est_lu=false` - Filtrer les non lus
- `GET    /api/contacts/non_lus/` - Messages non lus

### 🔗 Réseaux Sociaux
- `GET    /api/reseaux-sociaux/` - Liste tous les réseaux sociaux
- `POST   /api/reseaux-sociaux/` - Ajouter un réseau social
- `GET    /api/reseaux-sociaux/{id}/` - Détails
- `PUT    /api/reseaux-sociaux/{id}/` - Modifier
- `DELETE /api/reseaux-sociaux/{id}/` - Supprimer
- `GET    /api/reseaux-sociaux/?plateforme={nom}` - Filtrer par plateforme

### 📍 Localisations
- `GET    /api/localisations/` - Liste toutes les localisations
- `POST   /api/localisations/` - Créer une localisation
- `GET    /api/localisations/{id}/` - Détails
- `PUT    /api/localisations/{id}/` - Modifier
- `DELETE /api/localisations/{id}/` - Supprimer
- `GET    /api/localisations/?pays={nom}` - Filtrer par pays
- `GET    /api/localisations/actuelles/` - Localisations actuelles

---

## 🗂️ STRUCTURE DES DONNÉES

### Utilisateur
```json
{
  "id": 1,
  "nom": "Traore",
  "prenom": "Husseni",
  "photo_profil": null,
  "description": "Développeur Full Stack...",
  "age": 19,
  "email": "alhousein73@gmail.com",
  "lien_cv": "http://...",
  "telephone": "0586284129",
  "date_creation": "2026-01-12T10:30:00Z",
  "date_modification": "2026-01-12T10:30:00Z"
}
```

### Projet
```json
{
  "id": 1,
  "utilisateur": 1,
  "titre": "Portfolio Angular",
  "resume": "Portfolio moderne avec Angular 21",
  "image": null,
  "lien": "https://github.com/Eren-73/portfolio",
  "est_actif": true,
  "date_creation": "2026-01-12T10:30:00Z"
}
```

### Experience
```json
{
  "id": 1,
  "utilisateur": 1,
  "role": "Développeur Web",
  "description": "Stage de 4 mois...",
  "type_contrat": "STAGE",
  "date_debut": "2023-06-01",
  "date_fin": "2023-09-30",
  "entreprise": "PWA Energs",
  "est_en_cours": false
}
```

### Service
```json
{
  "id": 1,
  "utilisateur": 1,
  "nom": "Développement Backend Django",
  "detail": "Création d'API REST...",
  "type_service": "DEV_BACKEND",
  "outils": "Django, PostgreSQL, Docker",
  "est_disponible": true
}
```

### Contact
```json
{
  "id": 1,
  "utilisateur": 1,
  "nom_complet": "Jean Dupont",
  "email": "jean@example.com",
  "objet": "Demande de collaboration",
  "message": "Bonjour, je souhaiterais...",
  "est_lu": false,
  "date_envoi": "2026-01-12T10:30:00Z",
  "date_lecture": null
}
```

---

## 🧪 TESTER L'API

### Avec l'interface Browsable API (navigateur)

1. Ouvrez http://localhost:8000/api/
2. Cliquez sur les endpoints
3. Utilisez les formulaires pour créer/modifier des données

### Avec Postman ou Thunder Client

**Créer un utilisateur :**
```http
POST http://localhost:8000/api/utilisateurs/
Content-Type: application/json

{
    "nom": "Traore",
    "prenom": "Husseni",
    "age": 19,
    "email": "alhousein73@gmail.com",
    "telephone": "0586284129",
    "description": "Développeur Full Stack"
}
```

**Créer un projet :**
```http
POST http://localhost:8000/api/projets/
Content-Type: application/json

{
    "utilisateur": 1,
    "titre": "Mon Premier Projet",
    "resume": "Description du projet",
    "lien": "https://github.com/Eren-73/projet"
}
```

---

## 📚 DOCUMENTATION COMPLÈTE

Pour un **guide complet pour débutants** avec explications détaillées sur :
- Les Modèles Django
- Les Serializers
- Les Views et ViewSets
- Les URLs
- La configuration

👉 Consultez **[GUIDE_API_DJANGO.md](./GUIDE_API_DJANGO.md)**

---

## 🔧 COMMANDES UTILES

```powershell
# Créer de nouvelles migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver

# Ouvrir le shell Django
python manage.py shell

# Collecter les fichiers statiques
python manage.py collectstatic
```

---

## 📂 STRUCTURE DU PROJET

```
backend/
├── env/                     # Environnement virtuel
├── config/                  # Configuration Django
│   ├── settings.py         # Paramètres (CORS, REST, DB)
│   ├── urls.py             # URLs principales
│   ├── wsgi.py             # Déploiement WSGI
│   └── asgi.py             # Déploiement ASGI
├── api/                     # Application API
│   ├── migrations/         # Migrations de la base de données
│   ├── models.py           # 7 modèles (Utilisateur, Projet, etc.)
│   ├── serializers.py      # Conversion Python ↔ JSON
│   ├── views.py            # Logique métier (ViewSets)
│   ├── urls.py             # Routes de l'API
│   └── admin.py            # Interface admin
├── media/                   # Fichiers uploadés (images)
├── staticfiles/            # Fichiers statiques collectés
├── db.sqlite3              # Base de données SQLite
├── manage.py               # CLI Django
├── requirements.txt        # Dépendances Python
└── README.md               # Ce fichier
```

---

## 🌟 FONCTIONNALITÉS

✅ **7 modèles complets** avec relations (ForeignKey)  
✅ **CRUD complet** pour chaque modèle (Create, Read, Update, Delete)  
✅ **Filtrage avancé** par utilisateur, type, statut, etc.  
✅ **Actions personnalisées** (portfolio_complet, marquer_lu, etc.)  
✅ **Validation automatique** (email, URL, longueur, dates)  
✅ **Champs calculés** (nom_complet, est_en_cours, durée_mois)  
✅ **Interface admin complète** avec filtres et recherche  
✅ **CORS configuré** pour Angular  
✅ **Pagination automatique** (10 résultats par page)  
✅ **Upload d'images** (photo_profil, image de projet)  

---

## 🔐 SÉCURITÉ

⚠️ **En développement :**
- `DEBUG = True`
- Secret key exposée
- SQLite utilisé

🚀 **Pour la production, il faut :**
- Changer `DEBUG = False`
- Utiliser une vraie secret key (variables d'environnement)
- Utiliser PostgreSQL
- Configurer HTTPS
- Ajouter l'authentification JWT

---

## 🤝 CONTRIBUTION

Projet créé par **Traore Husseni** - Développeur Full Stack

- 📧 Email: alhousein73@gmail.com
- 🐙 GitHub: https://github.com/Eren-73
- 💼 LinkedIn: www.linkedin.com/in/husseni-traoré-134291290

---

## 📄 LICENCE

Ce projet est créé à des fins éducatives et de portfolio.

---

**Bon développement ! 🚀**

