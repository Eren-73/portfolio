"""
Location: backend/api/serializers.py
Purpose: Convertit les modèles Python en JSON et vice-versa
Why: Interface entre les modèles Django et l'API REST
Relevant: models.py, views.py
"""

from rest_framework import serializers
from .models import (
    Utilisateur, Projet, Experience, Service,
    Contact, ReseauSocial, Localisation
)


class UtilisateurSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Utilisateur
    """
    # Champs calculés (lecture seule)
    nom_complet = serializers.SerializerMethodField()
    nombre_projets = serializers.SerializerMethodField()
    nombre_experiences = serializers.SerializerMethodField()
    
    class Meta:
        model = Utilisateur
        fields = '__all__'
        read_only_fields = ['date_creation', 'date_modification']
    
    def get_nom_complet(self, obj):
        """Retourne le nom complet"""
        return f"{obj.prenom} {obj.nom}"
    
    def get_nombre_projets(self, obj):
        """Compte le nombre de projets"""
        return obj.projets.count()
    
    def get_nombre_experiences(self, obj):
        """Compte le nombre d'expériences"""
        return obj.experiences.count()


class ProjetSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Projet
    """
    # Informations de l'utilisateur (lecture seule)
    utilisateur_nom = serializers.CharField(
        source='utilisateur.prenom',
        read_only=True
    )
    
    class Meta:
        model = Projet
        fields = '__all__'
        read_only_fields = ['date_creation', 'date_modification']
    
    def validate_titre(self, value):
        """Valide que le titre fait au moins 3 caractères"""
        if len(value) < 3:
            raise serializers.ValidationError(
                "Le titre doit faire au moins 3 caractères"
            )
        return value


class ExperienceSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Experience
    """
    # Champs calculés
    est_en_cours = serializers.BooleanField(read_only=True)
    duree_mois = serializers.SerializerMethodField()
    
    class Meta:
        model = Experience
        fields = '__all__'
        read_only_fields = ['date_creation', 'date_modification']
    
    def get_duree_mois(self, obj):
        """Calcule la durée en mois"""
        from datetime import date
        date_fin = obj.date_fin or date.today()
        delta = date_fin - obj.date_debut
        return delta.days // 30
    
    def validate(self, data):
        """Valide que date_fin > date_debut"""
        if data.get('date_fin') and data.get('date_debut'):
            if data['date_fin'] < data['date_debut']:
                raise serializers.ValidationError(
                    "La date de fin doit être après la date de début"
                )
        return data


class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Service
    """
    # Liste des outils (converti de string à liste)
    outils_liste = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['date_creation', 'date_modification']
    
    def get_outils_liste(self, obj):
        """Convertit la chaîne d'outils en liste"""
        if obj.outils:
            return [outil.strip() for outil in obj.outils.split(',')]
        return []


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Contact
    """
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['date_envoi', 'date_lecture']
    
    def validate_message(self, value):
        """Valide que le message fait au moins 10 caractères"""
        if len(value) < 10:
            raise serializers.ValidationError(
                "Le message doit faire au moins 10 caractères"
            )
        return value


class ReseauSocialSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle ReseauSocial
    """
    class Meta:
        model = ReseauSocial
        fields = '__all__'
        read_only_fields = ['date_creation']


class LocalisationSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Localisation
    """
    # Adresse complète formatée
    adresse_complete = serializers.SerializerMethodField()
    
    class Meta:
        model = Localisation
        fields = '__all__'
        read_only_fields = ['date_creation']
    
    def get_adresse_complete(self, obj):
        """Retourne l'adresse complète formatée"""
        parties = []
        if obj.quartier:
            parties.append(obj.quartier)
        parties.append(obj.ville)
        parties.append(obj.pays)
        return ', '.join(parties)
    
    def validate(self, data):
        """Valide les coordonnées GPS"""
        lat = data.get('latitude')
        lon = data.get('longitude')
        
        if lat and (lat < -90 or lat > 90):
            raise serializers.ValidationError(
                "La latitude doit être entre -90 et 90"
            )
        
        if lon and (lon < -180 or lon > 180):
            raise serializers.ValidationError(
                "La longitude doit être entre -180 et 180"
            )
        
        return data
