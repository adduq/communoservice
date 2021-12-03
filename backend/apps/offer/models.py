from django.db import models
from django.contrib.auth.models import User


class StatusOffer(models.IntegerChoices):
    GIVEN = 0, 'Terminé'
    NOT_GIVEN = 1, 'Non terminé'
    CANCEL = 2, 'Annulé'
    NO_PRESENCE = 3, 'Non présenté'


class Offer(models.Model):
    """
    La classe offer permet d'avoir un détail complet de toutes les offres.
    """
    user = models.ForeignKey(User, related_name='offers',
                             db_column="id_user", on_delete=models.CASCADE)
    type_service = models.CharField(max_length=30, default="Administration")
    description = models.CharField(
        null=True, max_length=100, default="Aucune description")
    hourly_rate = models.DecimalField(
        null=True, max_digits=6, decimal_places=2)
    max_distance = models.PositiveIntegerField(null=True)
    date_added = models.DateField(auto_now_add=True)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    class Meta:
        ordering = ('-date_added',)


class ServiceType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'  # le f permet de formatter.

    # pour test
    def get_name(self):
        return self.name


class ActiveOffer(models.Model):
    """
    Permet de définir une offre active, c'est-à-dire une offre qui est
    actuellement disponible.
    """
    id_offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)


class ReservedOffer(models.Model):
    """
    Permet de définir une offre qui a été réservée.
    """
    id_offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    # Note:
    # ? Si suppression offre active -> courriel pour prévenir l'employeur ?
    id_active_offer = models.ForeignKey(ActiveOffer, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="employee_reserved_offer")
    id_recruiter = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name="recruiter_reserved_offer")
    reservation_date = models.DateField(null=True)
    hourly_rate = models.DecimalField(
        null=False, max_digits=6, decimal_places=2, default="13.50")


class TerminatedOffer(models.Model):
    """
    Permet de définir une offre qui a été terminée.
    """
    id_offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    id_active_offer = models.ForeignKey(
        ActiveOffer, on_delete=models.SET_NULL, null=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="employee_terminated_offer")
    id_recruiter = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name="recruiter_terminated_offer")
    completed_date = models.DateField(null=True)
    status = models.IntegerField(
        default=StatusOffer.GIVEN, choices=StatusOffer.choices)
    rating = models.FloatField(null=True)
    hourly_rate = models.DecimalField(
        null=False, max_digits=6, decimal_places=2, default="13.50")
