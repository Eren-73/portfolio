# Portfolio — Husseni Traore

Portfolio personnel full-stack avec Angular 21 (frontend) et Django 6 + REST Framework (backend).

---

## Démarrage rapide

### 1. Backend Django

```bash
cd backend
.\env\Scripts\activate          # Windows
python manage.py runserver      # → http://localhost:8000
```

### 2. Frontend Angular

```bash
# À la racine du projet
npm start                       # → http://localhost:4200
```

> Les deux doivent tourner en même temps pour que l'app fonctionne.

---

## Structure du projet

```
Portfolio/
├── backend/               ← API Django
│   ├── api/
│   │   ├── models.py      ← 7 modèles (Utilisateur, Projet, ...)
│   │   ├── serializers.py ← Conversion JSON
│   │   ├── views.py       ← Endpoints
│   │   └── urls.py        ← Routes
│   └── config/settings.py ← Configuration Django
└── src/app/
    ├── service/           ← Services Angular (1 par ressource API)
    ├── shared/
    │   ├── base/BaseService.ts  ← Client HTTP central
    │   └── models/        ← Interfaces TypeScript
    └── home/components/   ← Composants du portfolio
```

---

## Endpoints API

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/utilisateurs/` | Liste des utilisateurs |
| GET | `/api/utilisateurs/2/` | Profil de Husseni |
| GET | `/api/utilisateurs/2/portfolio_complet/` | Tout le portfolio en 1 appel |
| GET | `/api/projets/?utilisateur=2` | Projets filtrés |
| GET | `/api/experiences/?utilisateur=2` | Expériences |
| GET | `/api/services/?utilisateur=2` | Services |
| GET | `/api/reseaux-sociaux/?utilisateur=2` | Réseaux sociaux |
| POST | `/api/contacts/` | Envoyer un message |

API navigable dans le browser: **http://localhost:8000/api/**

---

## Gérer le contenu (Admin Django)

1. Va sur **http://localhost:8000/admin/**
2. Connecte-toi avec `admin` / `admin123`
3. Tu peux ajouter/modifier/supprimer:
   - **Projets** → apparaissent immédiatement dans le Portfolio
   - **Services** → s'affichent dans la section Services
   - **Expériences** → visibles dans Resume
   - **Contacts reçus** → messages envoyés depuis le formulaire

---

## ID utilisateur

Ton compte: **id=2** (email: `alhousein73@gmail.com`)

`USER_ID = 2` est défini dans chaque composant Angular:
- `about.ts`
- `portfolio.ts`
- `services.ts`
- `contact.ts`

---

## Modifier les données perso

Pour changer ton nom, description, email, âge etc. :

```
Django Admin → Utilisateurs → Husseni Traore → Modifier
```

---

## Ajouter un projet

1. Django Admin → Projets → Ajouter
2. Remplis: Titre, Résumé, Lien GitHub, Image (optionnel)
3. Sélectionne `Utilisateur` = Husseni Traore
4. Sauvegarde → le projet s'affiche automatiquement sur le portfolio

---

## Schéma de flux simple

```
Visiteur → Angular (port 4200)
              ↓ HTTP GET/POST
         Django API (port 8000)
              ↓
          SQLite (db.sqlite3)
```


## Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Vitest](https://vitest.dev/) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
