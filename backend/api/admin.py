"""
Location: backend/api/admin.py
Purpose: Configuration de l'interface d'administration Django
Why: Permet de gérer toutes les données du portfolio via l'admin
Relevant: models.py
"""

from django.contrib import admin
from django.utils import timezone
from django import forms
from .models import (
    Utilisateur, Projet, Experience, Service,
    Contact, ReseauSocial, Localisation
)


# ─────────────────────────────────────────────
# INLINES — gérables directement depuis l'utilisateur
# ─────────────────────────────────────────────

class ProjetInline(admin.TabularInline):
    """Projets affichés directement sur la page utilisateur"""
    model = Projet
    extra = 1  # 1 ligne vide pour ajouter rapidement
    fields = ['titre', 'resume', 'lien', 'image', 'est_actif']
    show_change_link = True  # lien vers la page détail du projet


class FormationInlineForm(forms.ModelForm):
    """Force type_contrat = FORMATION pour les entrées du bloc Éducation"""
    class Meta:
        model = Experience
        fields = ['role', 'entreprise', 'date_debut', 'date_fin', 'description']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.type_contrat = 'FORMATION'
        if commit:
            instance.save()
        return instance


class FormationInline(admin.TabularInline):
    """Formations / Études — type FORMATION uniquement"""
    model = Experience
    form = FormationInlineForm
    verbose_name = "Formation / Étude"
    verbose_name_plural = "Éducation (Formations & Études)"
    extra = 1
    fields = ['role', 'entreprise', 'date_debut', 'date_fin', 'description']
    show_change_link = True

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type_contrat='FORMATION')


class ExperienceInline(admin.TabularInline):
    """Expériences professionnelles (CDI, CDD, Stage, Alternance, Freelance)"""
    model = Experience
    verbose_name = "Expérience"
    verbose_name_plural = "Expériences Professionnelles"
    extra = 1
    fields = ['role', 'entreprise', 'type_contrat', 'date_debut', 'date_fin']
    show_change_link = True

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(type_contrat='FORMATION')


class ServiceInline(admin.TabularInline):
    """Services / Compétences — avec niveau de maîtrise en %"""
    model = Service
    extra = 1
    fields = ['nom', 'type_service', 'niveau', 'outils', 'est_disponible']
    show_change_link = True


class ReseauSocialInline(admin.TabularInline):
    """Réseaux sociaux affichés directement sur la page utilisateur"""
    model = ReseauSocial
    extra = 1
    fields = ['nom_plateforme', 'lien', 'est_actif']


class LocalisationInline(admin.TabularInline):
    """Localisation affichée directement sur la page utilisateur"""
    model = Localisation
    extra = 0
    fields = ['pays', 'ville', 'quartier', 'est_actuelle']


# ─────────────────────────────────────────────
# UTILISATEUR — page principale avec tout dedans
# ─────────────────────────────────────────────

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    """
    Page principale : on gère TOUT le portfolio depuis ici.
    Projets, expériences, services, réseaux sociaux → tout en bas de page.
    """
    list_display = ['prenom', 'nom', 'email', 'age', 'telephone', 'date_creation']
    search_fields = ['nom', 'prenom', 'email']
    readonly_fields = ['date_creation', 'date_modification']

    # Tous les sous-modèles sont éditables directement ici
    inlines = [
        ProjetInline,
        FormationInline,
        ExperienceInline,
        ServiceInline,
        ReseauSocialInline,
        LocalisationInline,
    ]

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'age', 'photo_profil')
        }),
        ('Contact', {
            'fields': ('email', 'telephone', 'lien_cv', 'fichier_cv')
        }),
        ('Description (affiché dans la section About)', {
            'fields': ('description',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )


# ─────────────────────────────────────────────
# PAGES DÉDIÉES (pour les vues liste complètes)
# ─────────────────────────────────────────────

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ['titre', 'utilisateur', 'est_actif', 'date_creation']
    list_filter = ['est_actif', 'utilisateur']
    search_fields = ['titre', 'resume']
    readonly_fields = ['date_creation', 'date_modification']
    list_editable = ['est_actif']  # modifiable directement dans la liste

    fieldsets = (
        ('Informations du projet', {
            'fields': ('utilisateur', 'titre', 'resume', 'lien')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Statut', {
            'fields': ('est_actif',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['role', 'entreprise', 'utilisateur', 'type_contrat', 'date_debut', 'date_fin', 'afficher_en_cours']
    list_filter = ['type_contrat', 'utilisateur']
    search_fields = ['role', 'entreprise']
    readonly_fields = ['date_creation', 'date_modification']
    date_hierarchy = 'date_debut'

    fieldsets = (
        ('Poste', {
            'fields': ('utilisateur', 'role', 'entreprise', 'type_contrat')
        }),
        ('Période', {
            'fields': ('date_debut', 'date_fin')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(boolean=True, description='En cours')
    def afficher_en_cours(self, obj):
        return obj.est_en_cours


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['nom', 'utilisateur', 'type_service', 'est_disponible']
    list_filter = ['type_service', 'est_disponible', 'utilisateur']
    search_fields = ['nom', 'detail']
    readonly_fields = ['date_creation', 'date_modification']
    list_editable = ['est_disponible']  # modifiable directement dans la liste

    fieldsets = (
        ('Service', {
            'fields': ('utilisateur', 'nom', 'type_service')
        }),
        ('Détails', {
            'fields': ('detail', 'outils')
        }),
        ('Disponibilité', {
            'fields': ('est_disponible',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Messages reçus via le formulaire de contact"""
    list_display = ['nom_complet', 'email', 'objet', 'est_lu', 'date_envoi']
    list_filter = ['est_lu', 'date_envoi']
    search_fields = ['nom_complet', 'email', 'objet', 'message']
    readonly_fields = ['nom_complet', 'email', 'objet', 'message', 'date_envoi', 'date_lecture', 'utilisateur']
    date_hierarchy = 'date_envoi'
    actions = ['marquer_comme_lu', 'marquer_comme_non_lu']

    fieldsets = (
        ('Expéditeur', {
            'fields': ('nom_complet', 'email')
        }),
        ('Message', {
            'fields': ('utilisateur', 'objet', 'message')
        }),
        ('Statut lecture', {
            'fields': ('est_lu', 'date_envoi', 'date_lecture')
        }),
    )

    @admin.action(description="✔ Marquer comme lu")
    def marquer_comme_lu(self, request, queryset):
        queryset.update(est_lu=True, date_lecture=timezone.now())

    @admin.action(description="✘ Marquer comme non lu")
    def marquer_comme_non_lu(self, request, queryset):
        queryset.update(est_lu=False, date_lecture=None)


@admin.register(ReseauSocial)
class ReseauSocialAdmin(admin.ModelAdmin):
    list_display = ['nom_plateforme', 'utilisateur', 'lien', 'est_actif']
    list_filter = ['nom_plateforme', 'est_actif']
    list_editable = ['est_actif']
    readonly_fields = ['date_creation']


@admin.register(Localisation)
class LocalisationAdmin(admin.ModelAdmin):
    list_display = ['ville', 'pays', 'utilisateur', 'est_actuelle']
    list_filter = ['pays', 'est_actuelle']
    list_editable = ['est_actuelle']
    readonly_fields = ['date_creation']



