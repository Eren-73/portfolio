"""
Location: backend/api/models.py
Purpose: Définition de tous les modèles de données pour l'API Portfolio
Why: Structure la base de données et les relations entre entités
Relevant: serializers.py, views.py, admin.py
"""

from django.db import models
from django.core.validators import EmailValidator, URLValidator


class Utilisateur(models.Model):
    """
    Modèle représentant un utilisateur/portfolio owner
    Relation: 1 Utilisateur -> N (Projets, Experiences, Services, etc.)
    """
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    photo_profil = models.ImageField(
        upload_to='utilisateurs/photos/',
        blank=True,
        null=True,
        verbose_name="Photo de profil"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description/Bio"
    )
    age = models.PositiveIntegerField(verbose_name="Âge")
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        verbose_name="Email"
    )
    lien_cv = models.URLField(
        blank=True,
        validators=[URLValidator()],
        verbose_name="Lien CV (URL externe)"
    )
    fichier_cv = models.FileField(
        upload_to='cvs/',
        blank=True,
        null=True,
        verbose_name="CV (fichier PDF)"
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone"
    )
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Projet(models.Model):
    """
    Modèle représentant un projet du portfolio
    Relation: N Projets -> 1 Utilisateur
    """
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='projets',
        verbose_name="Utilisateur"
    )
    titre = models.CharField(max_length=200, verbose_name="Titre")
    resume = models.TextField(verbose_name="Résumé")
    image = models.ImageField(
        upload_to='projets/images/',
        blank=True,
        null=True,
        verbose_name="Image du projet"
    )
    lien = models.URLField(
        blank=True,
        validators=[URLValidator()],
        verbose_name="Lien du projet (GitHub, démo, etc.)"
    )
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    est_actif = models.BooleanField(default=True, verbose_name="Projet actif")
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
    
    def __str__(self):
        return self.titre


class Experience(models.Model):
    """
    Modèle représentant une expérience professionnelle
    Relation: N Expériences -> 1 Utilisateur
    """
    TYPE_CONTRAT_CHOICES = [
        ('CDI', 'CDI - Contrat à Durée Indéterminée'),
        ('CDD', 'CDD - Contrat à Durée Déterminée'),
        ('STAGE', 'Stage'),
        ('ALTERNANCE', 'Alternance'),
        ('FREELANCE', 'Freelance'),
        ('FORMATION', 'Formation / Études'),
    ]
    
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='experiences',
        verbose_name="Utilisateur"
    )
    role = models.CharField(max_length=200, verbose_name="Rôle/Poste")
    description = models.TextField(verbose_name="Description")
    type_contrat = models.CharField(
        max_length=20,
        choices=TYPE_CONTRAT_CHOICES,
        verbose_name="Type de contrat"
    )
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date de fin (vide si en cours)"
    )
    entreprise = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Entreprise"
    )
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_debut']
        verbose_name = "Expérience"
        verbose_name_plural = "Expériences"
    
    def __str__(self):
        return f"{self.role} - {self.entreprise or 'N/A'}"
    
    @property
    def est_en_cours(self):
        """Retourne True si l'expérience est encore en cours"""
        return self.date_fin is None


class Service(models.Model):
    """
    Modèle représentant un service proposé
    Relation: N Services -> 1 Utilisateur
    """
    TYPE_SERVICE_CHOICES = [
        ('DEV_WEB', 'Développement Web'),
        ('DEV_MOBILE', 'Développement Mobile'),
        ('DEV_BACKEND', 'Développement Backend'),
        ('DEV_FRONTEND', 'Développement Frontend'),
        ('API', 'Création d\'API'),
        ('CONSULTING', 'Consulting'),
        ('FORMATION', 'Formation'),
        ('MAINTENANCE', 'Maintenance'),
    ]
    
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name="Utilisateur"
    )
    nom = models.CharField(max_length=200, verbose_name="Nom du service")
    detail = models.TextField(verbose_name="Détails")
    type_service = models.CharField(
        max_length=20,
        choices=TYPE_SERVICE_CHOICES,
        verbose_name="Type de service"
    )
    outils = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Outils/Technologies utilisés",
        help_text="Séparer par des virgules"
    )
    niveau = models.PositiveIntegerField(
        default=80,
        verbose_name="Niveau de maîtrise (%)",
        help_text="Entre 0 et 100"
    )

    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    est_disponible = models.BooleanField(
        default=True,
        verbose_name="Service disponible"
    )
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Service"
        verbose_name_plural = "Services"
    
    def __str__(self):
        return self.nom


class Contact(models.Model):
    """
    Modèle représentant une prise de contact
    Relation: N Contacts -> 1 Utilisateur (destinataire)
    """
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='contacts_recus',
        verbose_name="Destinataire"
    )
    nom_complet = models.CharField(max_length=200, verbose_name="Nom complet")
    email = models.EmailField(
        validators=[EmailValidator()],
        verbose_name="Email de l'expéditeur"
    )
    objet = models.CharField(max_length=300, verbose_name="Objet")
    message = models.TextField(verbose_name="Message")
    
    # Métadonnées
    date_envoi = models.DateTimeField(auto_now_add=True)
    est_lu = models.BooleanField(default=False, verbose_name="Lu")
    date_lecture = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Date de lecture"
    )
    
    class Meta:
        ordering = ['-date_envoi']
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
    
    def __str__(self):
        return f"{self.nom_complet} - {self.objet}"


class ReseauSocial(models.Model):
    """
    Modèle représentant un réseau social
    Relation: N Réseaux Sociaux -> 1 Utilisateur
    """
    PLATEFORME_CHOICES = [
        ('GITHUB', 'GitHub'),
        ('LINKEDIN', 'LinkedIn'),
        ('TWITTER', 'Twitter/X'),
        ('FACEBOOK', 'Facebook'),
        ('INSTAGRAM', 'Instagram'),
        ('YOUTUBE', 'YouTube'),
        ('PORTFOLIO', 'Site Portfolio'),
        ('AUTRE', 'Autre'),
    ]
    
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='reseaux_sociaux',
        verbose_name="Utilisateur"
    )
    nom_plateforme = models.CharField(
        max_length=50,
        choices=PLATEFORME_CHOICES,
        verbose_name="Nom de la plateforme"
    )
    lien = models.URLField(
        validators=[URLValidator()],
        verbose_name="Lien du profil"
    )
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    est_actif = models.BooleanField(
        default=True,
        verbose_name="Lien actif"
    )
    
    class Meta:
        ordering = ['nom_plateforme']
        verbose_name = "Réseau Social"
        verbose_name_plural = "Réseaux Sociaux"
        unique_together = ['utilisateur', 'nom_plateforme']
    
    def __str__(self):
        return f"{self.nom_plateforme} - {self.utilisateur}"


class Localisation(models.Model):
    """
    Modèle représentant une localisation
    Relation: N Localisations -> 1 Utilisateur
    """
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='localisations',
        verbose_name="Utilisateur"
    )
    pays = models.CharField(max_length=100, verbose_name="Pays")
    ville = models.CharField(max_length=100, verbose_name="Ville")
    quartier = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Quartier"
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="Latitude"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="Longitude"
    )
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    est_actuelle = models.BooleanField(
        default=True,
        verbose_name="Localisation actuelle"
    )
    
    class Meta:
        ordering = ['-est_actuelle', '-date_creation']
        verbose_name = "Localisation"
        verbose_name_plural = "Localisations"
    
    def __str__(self):
        return f"{self.ville}, {self.pays}"

