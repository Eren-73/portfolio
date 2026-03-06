"""
Location: backend/api/views.py
Purpose: Définit les vues/endpoints de l'API REST
Why: Gère la logique métier et les réponses HTTP
Relevant: models.py, serializers.py, urls.py
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import (
    Utilisateur, Projet, Experience, Service,
    Contact, ReseauSocial, Localisation
)
from .serializers import (
    UtilisateurSerializer, ProjetSerializer, ExperienceSerializer,
    ServiceSerializer, ContactSerializer, ReseauSocialSerializer,
    LocalisationSerializer
)


class UtilisateurViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les utilisateurs
    
    Liste: GET /api/utilisateurs/
    Détails: GET /api/utilisateurs/{id}/
    Créer: POST /api/utilisateurs/
    Modifier: PUT /api/utilisateurs/{id}/
    Modifier partiellement: PATCH /api/utilisateurs/{id}/
    Supprimer: DELETE /api/utilisateurs/{id}/
    """
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    
    @action(detail=True, methods=['get'])
    def portfolio_complet(self, request, pk=None):
        """
        Endpoint personnalisé pour récupérer toutes les infos d'un utilisateur
        GET /api/utilisateurs/{id}/portfolio_complet/
        """
        utilisateur = self.get_object()
        
        data = {
            'utilisateur': UtilisateurSerializer(utilisateur).data,
            'projets': ProjetSerializer(
                utilisateur.projets.filter(est_actif=True),
                many=True
            ).data,
            'experiences': ExperienceSerializer(
                utilisateur.experiences.all(),
                many=True
            ).data,
            'services': ServiceSerializer(
                utilisateur.services.filter(est_disponible=True),
                many=True
            ).data,
            'reseaux_sociaux': ReseauSocialSerializer(
                utilisateur.reseaux_sociaux.filter(est_actif=True),
                many=True
            ).data,
            'localisations': LocalisationSerializer(
                utilisateur.localisations.filter(est_actuelle=True),
                many=True
            ).data,
        }
        
        return Response(data)


class ProjetViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les projets
    
    Liste: GET /api/projets/
    Détails: GET /api/projets/{id}/
    Créer: POST /api/projets/
    Modifier: PUT /api/projets/{id}/
    Supprimer: DELETE /api/projets/{id}/
    """
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer
    
    def get_queryset(self):
        """Filtre optionnel par utilisateur"""
        queryset = Projet.objects.all()
        user_id = self.request.query_params.get('utilisateur', None)
        
        if user_id:
            queryset = queryset.filter(utilisateur_id=user_id)
        
        return queryset
    
    @action(detail=False, methods=['get'], url_path='par-utilisateur/(?P<user_id>[^/.]+)')
    def par_utilisateur(self, request, user_id=None):
        """
        Récupère tous les projets d'un utilisateur
        GET /api/projets/par-utilisateur/{user_id}/
        """
        projets = Projet.objects.filter(utilisateur_id=user_id, est_actif=True)
        serializer = self.get_serializer(projets, many=True)
        return Response(serializer.data)


class ExperienceViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les expériences
    
    Liste: GET /api/experiences/
    Détails: GET /api/experiences/{id}/
    Créer: POST /api/experiences/
    Modifier: PUT /api/experiences/{id}/
    Supprimer: DELETE /api/experiences/{id}/
    """
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    
    def get_queryset(self):
        """Filtre optionnel par utilisateur"""
        queryset = Experience.objects.all()
        user_id = self.request.query_params.get('utilisateur', None)
        
        if user_id:
            queryset = queryset.filter(utilisateur_id=user_id)
        
        return queryset
    
    @action(detail=False, methods=['get'], url_path='par-utilisateur/(?P<user_id>[^/.]+)')
    def par_utilisateur(self, request, user_id=None):
        """
        Récupère toutes les expériences d'un utilisateur
        GET /api/experiences/par-utilisateur/{user_id}/
        """
        experiences = Experience.objects.filter(utilisateur_id=user_id)
        serializer = self.get_serializer(experiences, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def en_cours(self, request):
        """
        Récupère les expériences en cours (sans date_fin)
        GET /api/experiences/en_cours/
        """
        experiences = Experience.objects.filter(date_fin__isnull=True)
        serializer = self.get_serializer(experiences, many=True)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les services
    
    Liste: GET /api/services/
    Détails: GET /api/services/{id}/
    Créer: POST /api/services/
    Modifier: PUT /api/services/{id}/
    Supprimer: DELETE /api/services/{id}/
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    
    def get_queryset(self):
        """Filtre optionnel par type ou utilisateur"""
        queryset = Service.objects.all()
        
        type_service = self.request.query_params.get('type', None)
        user_id = self.request.query_params.get('utilisateur', None)
        
        if type_service:
            queryset = queryset.filter(type_service=type_service)
        
        if user_id:
            queryset = queryset.filter(utilisateur_id=user_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """
        Récupère les services disponibles
        GET /api/services/disponibles/
        """
        services = Service.objects.filter(est_disponible=True)
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)


class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les prises de contact
    
    Liste: GET /api/contacts/
    Détails: GET /api/contacts/{id}/
    Créer: POST /api/contacts/
    Marquer comme lu: PATCH /api/contacts/{id}/marquer_lu/
    Supprimer: DELETE /api/contacts/{id}/
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    
    def get_queryset(self):
        """Filtre optionnel par statut de lecture"""
        queryset = Contact.objects.all()
        
        est_lu = self.request.query_params.get('est_lu', None)
        user_id = self.request.query_params.get('utilisateur', None)
        
        if est_lu is not None:
            est_lu_bool = est_lu.lower() == 'true'
            queryset = queryset.filter(est_lu=est_lu_bool)
        
        if user_id:
            queryset = queryset.filter(utilisateur_id=user_id)
        
        return queryset
    
    @action(detail=True, methods=['patch'])
    def marquer_lu(self, request, pk=None):
        """
        Marque un message comme lu
        PATCH /api/contacts/{id}/marquer_lu/
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


class ReseauSocialViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les réseaux sociaux
    
    Liste: GET /api/reseaux-sociaux/
    Détails: GET /api/reseaux-sociaux/{id}/
    Créer: POST /api/reseaux-sociaux/
    Modifier: PUT /api/reseaux-sociaux/{id}/
    Supprimer: DELETE /api/reseaux-sociaux/{id}/
    """
    queryset = ReseauSocial.objects.all()
    serializer_class = ReseauSocialSerializer
    
    def get_queryset(self):
        """Filtre optionnel par utilisateur"""
        queryset = ReseauSocial.objects.all()
        
        user_id = self.request.query_params.get('utilisateur', None)
        plateforme = self.request.query_params.get('plateforme', None)
        
        if user_id:
            queryset = queryset.filter(utilisateur_id=user_id)
        
        if plateforme:
            queryset = queryset.filter(nom_plateforme=plateforme)
        
        return queryset


class LocalisationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les localisations
    
    Liste: GET /api/localisations/
    Détails: GET /api/localisations/{id}/
    Créer: POST /api/localisations/
    Modifier: PUT /api/localisations/{id}/
    Supprimer: DELETE /api/localisations/{id}/
    """
    queryset = Localisation.objects.all()
    serializer_class = LocalisationSerializer
    
    def get_queryset(self):
        """Filtre optionnel par utilisateur"""
        queryset = Localisation.objects.all()
        
        user_id = self.request.query_params.get('utilisateur', None)
        pays = self.request.query_params.get('pays', None)
        actuelle = self.request.query_params.get('actuelle', None)
        
        if user_id:
            queryset = queryset.filter(utilisateur_id=user_id)
        
        if pays:
            queryset = queryset.filter(pays__icontains=pays)
        
        if actuelle is not None:
            actuelle_bool = actuelle.lower() == 'true'
            queryset = queryset.filter(est_actuelle=actuelle_bool)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def actuelles(self, request):
        """
        Récupère les localisations actuelles
        GET /api/localisations/actuelles/
        """
        localisations = Localisation.objects.filter(est_actuelle=True)
        serializer = self.get_serializer(localisations, many=True)
        return Response(serializer.data)

