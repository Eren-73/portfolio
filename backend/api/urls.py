"""
Location: backend/api/urls.py
Purpose: Configuration des routes/endpoints de l'API
Why: Mappe les URLs aux vues correspondantes
Relevant: views.py, config/urls.py
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UtilisateurViewSet, ProjetViewSet, ExperienceViewSet,
    ServiceViewSet, ContactViewSet, ReseauSocialViewSet,
    LocalisationViewSet
)

# Router REST Framework pour les ViewSets
router = DefaultRouter()

# Enregistrement des ViewSets
router.register(r'utilisateurs', UtilisateurViewSet, basename='utilisateur')
router.register(r'projets', ProjetViewSet, basename='projet')
router.register(r'experiences', ExperienceViewSet, basename='experience')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'reseaux-sociaux', ReseauSocialViewSet, basename='reseau-social')
router.register(r'localisations', LocalisationViewSet, basename='localisation')

# URLs de l'app
urlpatterns = [
    path('', include(router.urls)),
]
