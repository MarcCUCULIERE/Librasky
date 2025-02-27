# Librasky - Gestionnaire de Cave à Whisky

Librasky est une application web permettant de gérer votre collection de whiskies. Elle permet de cataloguer, organiser et suivre votre cave à whisky avec des fonctionnalités d'import/export et de gestion d'images.

## Technologies Utilisées

### Backend
- Python 3.9+
- FastAPI (Framework API REST)
- SQLAlchemy (ORM)
- SQLite (Base de données)
- Swagger/OpenAPI (Documentation API)
- Pydantic (Validation des données)
- Python-multipart (Gestion des uploads)

### Frontend
- Angular 15+
- Angular Material (UI Components)
- RxJS (Programmation réactive)
- NgRx (Gestion d'état)

## Structure du Projet

## Installation

### Prérequis
- Python 3.9+
- Node.js 16+
- npm 8+

### Installation du Backend

1. Créer un environnement virtuel Python
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

2. Installer les dépendances
```bash
pip install -r requirements.txt
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

3. Initialiser la base de données
```bash
python app/database.py

4. Lancer le serveur de développement
uvicorn app.main:app --reload
Le backend sera accessible sur http://localhost:8000 La documentation Swagger sera disponible sur http://localhost:8000/docs

### Installation du Frontend

1. Installer les dépendances    
   cd frontend
   npm install

2. Lancer le serveur de développement
   npm start
   Le frontend sera accessible sur http://localhost:4200

## Fonctionnalités Principales

Gestion des Whiskies
- Ajout/Modification/Suppression de whiskies
- Upload d'images
- Informations détaillées (nom, distillerie, année, notes de dégustation, etc.)
- Système de catégorisation
Import/Export
- Export de la collection au format JSON (incluant les images en base64)
- Import de collections au format JSON
- Validation des données importées
Interface Utilisateur
- Interface responsive
- Recherche et filtrage
- Visualisation en mode grille/liste
- Gestion des images avec prévisualisation

### API Documentation
- La documentation Swagger est disponible sur http://localhost:8000/docs
- Les endpoints disponibles sont :
  - GET /api/v1/items : Récupérer la liste des items
  - POST /api/v1/items : Créer un nouvel item
  - GET /api/v1/items/{item_id} : Récupérer un item par son ID
  - PUT /api/v1/items/{item_id} : Mettre à jour un item par son ID
  - DELETE /api/v1/items/{item_id} : Supprimer un item par son ID
  - POST /api/v1/items/import : Importer des items à partir d'un fichier JSON
  - GET /api/v1/items/export : Exporter les items au format JSON

### Development

### License

This project is licensed under the MIT License. See the LICENSE file for details.



TODO:
- [x] Configurer la base de données SQLite
- [x] Implémenter les routes API dans le backend
- [x] Implémenter la logique d'import/export
- [X] Créer les composants Angular pour le frontend
- [x] Mettre en place la documentation Swagger
- [x] Configurer la base de données SQLite
- [ ] Implémenter la logique d'import/export
- [ ] Ajouter des tests unitaires
- [ ] Ajouter des tests d'intégration
- [ ] Ajouter des tests de performance
- [ ] Ajouter des tests de sécurité
- [ ] Ajouter des tests de compatibilité
- [ ] Ajouter des tests de régression
- [ ] Ajouter des tests de charge
- [ ] Ajouter des tests de stress
Ajouter l'authentification
Implémenter la pagination côté frontend
Ajouter des filtres avancés
Créer une vue détaillée pour chaque whisky
Ajouter des statistiques et des graphiques
Implémenter un système de tags/catégories
Ajouter des tests unitaires et e2e