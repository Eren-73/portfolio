# 📚 GUIDE COMPLET - API DJANGO REST FRAMEWORK POUR DÉBUTANTS

## 🎯 OBJECTIF DU PROJET

Nous avons créé une **API REST complète** pour un portfolio professionnel.

Cette API permet de :
- Gérer les informations d'un utilisateur (développeur)
- Afficher ses projets, expériences, services
- Recevoir des messages de contact
- Gérer ses réseaux sociaux et localisations

---

## 📖 TABLE DES MATIÈRES

1. [Structure du Projet](#1-structure-du-projet)
2. [Les Modèles Django (models.py)](#2-les-modèles-django-modelspy)
3. [Les Serializers (serializers.py)](#3-les-serializers-serializerspy)
4. [Les Views (views.py)](#4-les-views-viewspy)
5. [Les URLs (urls.py)](#5-les-urls-urlspy)
6. [Configuration (settings.py)](#6-configuration-settingspy)
7. [Interface Admin (admin.py)](#7-interface-admin-adminpy)
8. [Comment Utiliser l'API](#8-comment-utiliser-lapi)

---

## 1. STRUCTURE DU PROJET

```
backend/
├── env/                    # Environnement virtuel Python
├── config/                 # Configuration Django
│   ├── settings.py        # Paramètres globaux
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Déploiement
├── api/                    # Notre application
│   ├── migrations/        # Historique des changements de BDD
│   ├── models.py          # Structure des données
│   ├── serializers.py     # Conversion Python ↔ JSON
│   ├── views.py           # Logique métier
│   ├── urls.py            # Routes de l'API
│   └── admin.py           # Interface d'administration
├── manage.py              # Commandes Django
├── requirements.txt       # Dépendances Python
└── db.sqlite3            # Base de données
```

---

## 2. LES MODÈLES DJANGO (models.py)

### 🤔 QU'EST-CE QU'UN MODÈLE ?

Un **modèle** est une **classe Python** qui représente une **table dans la base de données**.

Chaque **attribut** de la classe = une **colonne** dans la table.

### 📝 EXEMPLE SIMPLE

```python
class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    email = models.EmailField(unique=True)
```

Ceci crée une table avec 3 colonnes : `nom`, `age`, `email`.

### 🔍 LES 7 MODÈLES DE NOTRE API

#### 1️⃣ **Utilisateur** (Le développeur)
```python
class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    photo_profil = models.ImageField(upload_to='utilisateurs/photos/', blank=True)
    description = models.TextField(blank=True)
    age = models.PositiveIntegerField()
    email = models.EmailField(unique=True)
    lien_cv = models.URLField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
```

**Explication :**
- `CharField` = Texte court (nom, prénom)
- `TextField` = Texte long (description)
- `ImageField` = Image (photo de profil)
- `EmailField` = Email avec validation automatique
- `URLField` = URL avec validation automatique
- `PositiveIntegerField` = Nombre entier positif
- `blank=True` = Champ optionnel
- `unique=True` = Valeur unique dans toute la table
- `auto_now_add=True` = Date ajoutée automatiquement à la création
- `auto_now=True` = Date mise à jour automatiquement à chaque modification

#### 2️⃣ **Projet** (Un projet GitHub, démo, etc.)
```python
class Projet(models.Model):
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='projets'
    )
    titre = models.CharField(max_length=200)
    resume = models.TextField()
    image = models.ImageField(upload_to='projets/images/', blank=True)
    lien = models.URLField(blank=True)
    est_actif = models.BooleanField(default=True)
```

**Explication de ForeignKey :**
- `ForeignKey` = **Relation** entre 2 tables
- Un Utilisateur peut avoir **plusieurs** Projets
- `on_delete=models.CASCADE` = Si on supprime l'utilisateur, ses projets sont aussi supprimés
- `related_name='projets'` = Permet de faire `utilisateur.projets.all()` pour récupérer tous ses projets

**Relation :** 1 Utilisateur → N Projets

#### 3️⃣ **Experience** (Expérience professionnelle)
```python
class Experience(models.Model):
    TYPE_CONTRAT_CHOICES = [
        ('CDI', 'CDI - Contrat à Durée Indéterminée'),
        ('CDD', 'CDD - Contrat à Durée Déterminée'),
        ('STAGE', 'Stage'),
        ('ALTERNANCE', 'Alternance'),
        ('FREELANCE', 'Freelance'),
        ('INTERIM', 'Intérim'),
    ]
    
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='experiences')
    role = models.CharField(max_length=200)
    description = models.TextField()
    type_contrat = models.CharField(max_length=20, choices=TYPE_CONTRAT_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    entreprise = models.CharField(max_length=200, blank=True)
    
    @property
    def est_en_cours(self):
        """Retourne True si l'expérience est encore en cours"""
        return self.date_fin is None
```

**Explication :**
- `choices=TYPE_CONTRAT_CHOICES` = Liste déroulante avec des valeurs prédéfinies
- `DateField` = Date seulement (pas d'heure)
- `null=True` = Peut être NULL dans la base de données
- `@property` = Méthode qui se comporte comme un attribut (pas besoin de `()`)

#### 4️⃣ **Service** (Compétences/Services proposés)
```python
class Service(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='services')
    nom = models.CharField(max_length=200)
    detail = models.TextField()
    type_service = models.CharField(max_length=20, choices=TYPE_SERVICE_CHOICES)
    outils = models.CharField(max_length=500, blank=True)
    est_disponible = models.BooleanField(default=True)
```

#### 5️⃣ **Contact** (Messages reçus)
```python
class Contact(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='contacts_recus')
    nom_complet = models.CharField(max_length=200)
    email = models.EmailField()
    objet = models.CharField(max_length=300)
    message = models.TextField()
    est_lu = models.BooleanField(default=False)
    date_envoi = models.DateTimeField(auto_now_add=True)
    date_lecture = models.DateTimeField(blank=True, null=True)
```

#### 6️⃣ **ReseauSocial** (Liens GitHub, LinkedIn, etc.)
```python
class ReseauSocial(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='reseaux_sociaux')
    nom_plateforme = models.CharField(max_length=50, choices=PLATEFORME_CHOICES)
    lien = models.URLField()
    est_actif = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['utilisateur', 'nom_plateforme']  # Un utilisateur ne peut pas avoir 2 fois le même réseau social
```

#### 7️⃣ **Localisation** (Où habite le développeur)
```python
class Localisation(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='localisations')
    pays = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    quartier = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    est_actuelle = models.BooleanField(default=True)
```

### 📊 RÉSUMÉ DES RELATIONS

```
Utilisateur (1) ─────► (N) Projets
            │
            ├─────► (N) Experiences
            │
            ├─────► (N) Services
            │
            ├─────► (N) Contacts
            │
            ├─────► (N) ReseauSocial
            │
            └─────► (N) Localisations
```

---

## 3. LES SERIALIZERS (serializers.py)

### 🤔 QU'EST-CE QU'UN SERIALIZER ?

Un **Serializer** est un **traducteur** entre Python et JSON.

```
Python Object (Modèle) ←→ JSON (API)
```

**Exemple :**

```python
# Objet Python (Modèle Django)
utilisateur = Utilisateur(nom="Traore", prenom="Husseni", age=19)

# Serializer le transforme en JSON
{
    "nom": "Traore",
    "prenom": "Husseni",
    "age": 19
}
```

### 📝 ANATOMIE D'UN SERIALIZER

```python
class UtilisateurSerializer(serializers.ModelSerializer):
    # Champs calculés (pas dans le modèle, mais dans le JSON)
    nom_complet = serializers.SerializerMethodField()
    
    class Meta:
        model = Utilisateur  # Quel modèle on sérialise
        fields = '__all__'   # Tous les champs du modèle
        read_only_fields = ['date_creation', 'date_modification']  # Ces champs ne peuvent pas être modifiés
    
    def get_nom_complet(self, obj):
        """Méthode pour le champ calculé nom_complet"""
        return f"{obj.prenom} {obj.nom}"
```

**Résultat JSON :**
```json
{
    "id": 1,
    "nom": "Traore",
    "prenom": "Husseni",
    "age": 19,
    "email": "alhousein73@gmail.com",
    "nom_complet": "Husseni Traore",  ← Champ calculé
    "date_creation": "2026-01-12T10:30:00Z",
    "date_modification": "2026-01-12T10:30:00Z"
}
```

### 🔍 LES DIFFÉRENTS TYPES DE CHAMPS

#### 1️⃣ **SerializerMethodField** (Champ calculé)
```python
nom_complet = serializers.SerializerMethodField()

def get_nom_complet(self, obj):
    return f"{obj.prenom} {obj.nom}"
```
→ Crée un champ qui n'existe pas dans le modèle, calculé dynamiquement.

#### 2️⃣ **CharField** (avec source)
```python
utilisateur_nom = serializers.CharField(
    source='utilisateur.prenom',
    read_only=True
)
```
→ Récupère une valeur depuis une relation ForeignKey.

#### 3️⃣ **Validation personnalisée**
```python
def validate_titre(self, value):
    """Valide que le titre fait au moins 3 caractères"""
    if len(value) < 3:
        raise serializers.ValidationError(
            "Le titre doit faire au moins 3 caractères"
        )
    return value
```
→ Django appelle automatiquement `validate_<nom_du_champ>` avant de sauvegarder.

#### 4️⃣ **Validation globale**
```python
def validate(self, data):
    """Valide plusieurs champs ensemble"""
    if data.get('date_fin') and data.get('date_debut'):
        if data['date_fin'] < data['date_debut']:
            raise serializers.ValidationError(
                "La date de fin doit être après la date de début"
            )
    return data
```

### 🎓 EXEMPLE COMPLET : ProjetSerializer

```python
class ProjetSerializer(serializers.ModelSerializer):
    # Champ calculé : nom de l'utilisateur qui a créé le projet
    utilisateur_nom = serializers.CharField(
        source='utilisateur.prenom',
        read_only=True
    )
    
    class Meta:
        model = Projet
        fields = '__all__'  # Tous les champs
        read_only_fields = ['date_creation', 'date_modification']
    
    def validate_titre(self, value):
        """Le titre doit faire au moins 3 caractères"""
        if len(value) < 3:
            raise serializers.ValidationError(
                "Le titre doit faire au moins 3 caractères"
            )
        return value
```

**Ce que fait ce Serializer :**
1. Convertit un objet Projet en JSON
2. Ajoute le nom de l'utilisateur dans le JSON
3. Empêche la modification de `date_creation` et `date_modification`
4. Valide que le titre a au moins 3 caractères

---

## 4. LES VIEWS (views.py)

### 🤔 QU'EST-CE QU'UNE VIEW ?

Une **View** est une **fonction ou classe** qui :
1. Reçoit une requête HTTP (GET, POST, PUT, DELETE)
2. Traite la demande (lecture/écriture en base de données)
3. Retourne une réponse HTTP (JSON)

### 📝 TYPES DE VIEWS

#### 1️⃣ **ViewSet** (Le plus puissant)

Un **ViewSet** crée automatiquement **5 endpoints** :
- `GET /api/projets/` → Liste tous les projets
- `POST /api/projets/` → Créer un projet
- `GET /api/projets/1/` → Détails du projet 1
- `PUT /api/projets/1/` → Modifier le projet 1
- `DELETE /api/projets/1/` → Supprimer le projet 1

**Code :**
```python
class ProjetViewSet(viewsets.ModelViewSet):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer
```

C'est tout ! Django REST Framework crée les 5 endpoints automatiquement.

#### 2️⃣ **Filtrage avec get_queryset()**

```python
class ProjetViewSet(viewsets.ModelViewSet):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer
    
    def get_queryset(self):
        """Filtre les projets par utilisateur si demandé"""
        queryset = Projet.objects.all()
        user_id = self.request.query_params.get('utilisateur', None)
        
        if user_id:
            queryset = queryset.filter(utilisateur_id=user_id)
        
        return queryset
```

**Utilisation :**
- `GET /api/projets/` → Tous les projets
- `GET /api/projets/?utilisateur=1` → Projets de l'utilisateur 1 seulement

#### 3️⃣ **Actions personnalisées avec @action**

```python
class ProjetViewSet(viewsets.ModelViewSet):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer
    
    @action(detail=False, methods=['get'], url_path='par-utilisateur/(?P<user_id>[^/.]+)')
    def par_utilisateur(self, request, user_id=None):
        """
        Récupère tous les projets d'un utilisateur
        GET /api/projets/par-utilisateur/1/
        """
        projets = Projet.objects.filter(utilisateur_id=user_id, est_actif=True)
        serializer = self.get_serializer(projets, many=True)
        return Response(serializer.data)
```

**Explication :**
- `detail=False` → Endpoint sans ID (pas `/api/projets/1/action/`)
- `detail=True` → Endpoint avec ID (`/api/projets/1/action/`)
- `methods=['get']` → Méthode HTTP autorisée
- `url_path` → Chemin personnalisé dans l'URL

### 🎓 EXEMPLE COMPLET : ContactViewSet

```python
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    
    def get_queryset(self):
        """Filtre par statut de lecture"""
        queryset = Contact.objects.all()
        est_lu = self.request.query_params.get('est_lu', None)
        
        if est_lu is not None:
            est_lu_bool = est_lu.lower() == 'true'
            queryset = queryset.filter(est_lu=est_lu_bool)
        
        return queryset
    
    @action(detail=True, methods=['patch'])
    def marquer_lu(self, request, pk=None):
        """
        Marque un message comme lu
        PATCH /api/contacts/1/marquer_lu/
        """
        contact = self.get_object()
        contact.est_lu = True
        contact.date_lecture = timezone.now()
        contact.save()
        
        serializer = self.get_serializer(contact)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def non_lus(self, request):
        """
        Récupère les messages non lus
        GET /api/contacts/non_lus/
        """
        contacts = Contact.objects.filter(est_lu=False)
        serializer = self.get_serializer(contacts, many=True)
        return Response(serializer.data)
```

**Endpoints créés :**
- `GET /api/contacts/` → Liste (filtre avec `?est_lu=false`)
- `POST /api/contacts/` → Créer
- `GET /api/contacts/1/` → Détails
- `PATCH /api/contacts/1/marquer_lu/` → **Action personnalisée**
- `GET /api/contacts/non_lus/` → **Action personnalisée**

---

## 5. LES URLs (urls.py)

### 🤔 QU'EST-CE QU'UNE URL ?

Une **URL** est un **chemin** qui mappe une adresse web vers une View.

```
http://localhost:8000/api/projets/ → ProjetViewSet
```

### 📝 CONFIGURATION DES URLs

#### Dans `api/urls.py` :
```python
from rest_framework.routers import DefaultRouter
from .views import ProjetViewSet, ExperienceViewSet

# Créer un router
router = DefaultRouter()

# Enregistrer les ViewSets
router.register(r'projets', ProjetViewSet, basename='projet')
router.register(r'experiences', ExperienceViewSet, basename='experience')

# URLs générées automatiquement
urlpatterns = [
    path('', include(router.urls)),
]
```

**Résultat :**
- `/api/projets/` → ProjetViewSet
- `/api/projets/1/` → Détails du projet 1
- `/api/experiences/` → ExperienceViewSet
- `/api/experiences/1/` → Détails de l'expérience 1

#### Dans `config/urls.py` :
```python
urlpatterns = [
    path('admin/', admin.site.urls),  # Interface admin
    path('api/', include('api.urls')),  # Toutes les URLs de l'API
]
```

---

## 6. CONFIGURATION (settings.py)

### 📝 INSTALLED_APPS

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',      # Django REST Framework
    'corsheaders',         # CORS (pour Angular)
    
    # Local apps
    'api.apps.ApiConfig',  # Notre app
]
```

### 📝 MIDDLEWARE (CORS)

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # DOIT être en premier
    'django.middleware.security.SecurityMiddleware',
    # ... autres middlewares
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',  # Angular
    'http://localhost:4201',
]
```

**Pourquoi CORS ?**
→ Par défaut, un site web ne peut pas faire de requêtes vers un autre domaine.
→ CORS autorise Angular (port 4201) à communiquer avec Django (port 8000).

### 📝 REST FRAMEWORK

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # 10 résultats par page
}
```

---

## 7. INTERFACE ADMIN (admin.py)

### 🤔 QU'EST-CE QUE L'ADMIN DJANGO ?

Une **interface web automatique** pour gérer les données sans coder.

### 📝 CONFIGURATION

```python
@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ['titre', 'utilisateur', 'est_actif', 'date_creation']
    list_filter = ['est_actif', 'date_creation']
    search_fields = ['titre', 'resume']
    readonly_fields = ['date_creation', 'date_modification']
```

**Explication :**
- `list_display` = Colonnes affichées dans la liste
- `list_filter` = Filtres sur le côté
- `search_fields` = Barre de recherche
- `readonly_fields` = Champs non modifiables

---

## 8. COMMENT UTILISER L'API

### 🚀 DÉMARRER LE SERVEUR

```bash
cd D:\Projets\Angular\Portfolio\backend
python manage.py runserver
```

### 📡 TESTER LES ENDPOINTS

#### 1️⃣ **Créer un utilisateur**
```http
POST http://localhost:8000/api/utilisateurs/
Content-Type: application/json

{
    "nom": "Traore",
    "prenom": "Husseni",
    "age": 19,
    "email": "alhousein73@gmail.com",
    "telephone": "0586284129",
    "description": "Développeur Full Stack passionné"
}
```

#### 2️⃣ **Lister tous les utilisateurs**
```http
GET http://localhost:8000/api/utilisateurs/
```

#### 3️⃣ **Créer un projet**
```http
POST http://localhost:8000/api/projets/
Content-Type: application/json

{
    "utilisateur": 1,
    "titre": "Portfolio Angular",
    "resume": "Un portfolio moderne avec Angular 21",
    "lien": "https://github.com/Eren-73/portfolio"
}
```

#### 4️⃣ **Récupérer tous les projets d'un utilisateur**
```http
GET http://localhost:8000/api/projets/?utilisateur=1
```

#### 5️⃣ **Portfolio complet (endpoint personnalisé)**
```http
GET http://localhost:8000/api/utilisateurs/1/portfolio_complet/
```

Retourne **TOUT** : utilisateur + projets + expériences + services + réseaux sociaux + localisations.

---

## 🎓 RÉSUMÉ DES CONCEPTS CLÉS

| Concept | Rôle | Fichier |
|---------|------|---------|
| **Modèle** | Structure de la base de données | `models.py` |
| **Serializer** | Traducteur Python ↔ JSON | `serializers.py` |
| **View** | Logique métier (requêtes HTTP) | `views.py` |
| **URL** | Chemin vers les Views | `urls.py` |
| **Admin** | Interface d'administration | `admin.py` |
| **Migration** | Historique des changements BDD | `migrations/` |

---

## 🔄 WORKFLOW COMPLET

```
1. Requête HTTP arrive → urls.py
                          ↓
2. Route vers la View → views.py
                          ↓
3. View interroge le Modèle → models.py
                          ↓
4. Modèle récupère les données → Base de données
                          ↓
5. Serializer transforme en JSON → serializers.py
                          ↓
6. Réponse HTTP envoyée → Client (Angular)
```

---

## 📚 COMMANDES UTILES

```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver

# Ouvrir le shell Django
python manage.py shell
```

---

## 🎯 PROCHAINES ÉTAPES

1. Tester tous les endpoints avec Postman ou l'interface DRF
2. Ajouter des données via l'admin Django
3. Connecter Angular à l'API
4. Ajouter l'authentification (JWT)
5. Déployer l'API en production

---

**Bravo ! Vous avez créé une API REST complète et professionnelle ! 🎉**
