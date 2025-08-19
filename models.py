from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid  # Importa il modulo uuid
from django.contrib.postgres.fields import JSONField # Importa il JSONField



class Organization(models.model):
    """
    Modello per rappresentare un'organizzazione.
    """
    # Usa un UUID come chiave primaria
    org_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('Organization ID'))
    name = models.CharField(max_length=200, unique=True, verbose_name=_('Organization Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')

    def __str__(self):
        return self.name



class Country(models.Model):
    """
    Modello per rappresentare una nazione.
    """
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    iso_code = models.CharField(max_length=2, verbose_name=_('ISO Code'))
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='countries', verbose_name=_('Organization'))

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        unique_together = ('iso_code', 'organization')

    def __str__(self):
        return self.name



class Address(models.Model):
    """
    Modello per rappresentare un indirizzo.
    """
    street = models.CharField(max_length=200, verbose_name=_('Street'))
    city = models.CharField(max_length=100, verbose_name=_('City'))
    zip_code = models.CharField(max_length=10, verbose_name=_('ZIP Code'))
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='addresses', verbose_name=_('Country'))
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='addresses', verbose_name=_('Organization'))

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return f"{self.street}, {self.city}, {self.zip_code}, {self.country}"


class Location(models.Model):
    """
    Modello per rappresentare una posizione geografica.
    """
    name = models.CharField(max_length=200, verbose_name=_('Location Name'))
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='locations', verbose_name=_('Organization'))
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True, related_name='location', verbose_name=_('Address'))

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        unique_together = ('name', 'organization')  # Una location deve essere unica per organizzazione

    def __str__(self):
        return f"{self.name} ({self.organization.name})"



class Permission(models.Model):
    """
    Modello per rappresentare un permesso personalizzato.
    """
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    api_name = models.CharField(max_length=100, blank=True, verbose_name=_('API Name'))
    type = models.CharField(max_length=30, verbose_name=_('Type'))
    obj = models.CharField(max_length=100, blank=True, default='Add obj tab name', verbose_name=_('Object'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Date'))
    modified_date = models.DateTimeField(auto_now=True, verbose_name=_('Modified Date'))
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='permissions', verbose_name=_('Organization'))

    class Meta:
        verbose_name = _('Permission')
        verbose_name_plural = _('Permissions')
        unique_together = ('api_name', 'organization')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Sovrascrive il metodo save() per generare automaticamente l'api_name.
        """
        if not self.api_name:
            self.api_name = self.name.strip().replace(' ', '_').lower()
        super().save(*args, **kwargs)



class Role(models.Model):
    """
    Modello per rappresentare un ruolo all'interno di un'organizzazione.
    """
    name = models.CharField(max_length=100, verbose_name=_('Role Name'))
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='roles', verbose_name=_('Organization'))
    permissions = models.ManyToManyField(Permission, blank=True, related_name='roles', verbose_name=_('Permissions'))

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        unique_together = ('name', 'organization')  # Un ruolo deve essere unico per organizzazione

    def __str__(self):
        return self.name



class Drone(models.Model):
    """
    Modello per rappresentare un drone.
    """
    name = models.CharField(max_length=100, verbose_name=_('Drone Name'))
    model = models.CharField(max_length=100, verbose_name=_('Drone Model'))
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='drones', verbose_name=_('Location'))
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='drones', verbose_name=_('Organization'))

    class Meta:
        verbose_name = _('Drone')
        verbose_name_plural = _('Drones')

    def __str__(self):
        return self.name



class Iot(models.Model):
    """
    Modello per rappresentare un dispositivo IoT.
    """
    name = models.CharField(max_length=100, verbose_name=_('IoT Device Name'))
    model = models.CharField(max_length=100, verbose_name=_('IoT Device Model'))
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='iots', verbose_name=_('Location'))
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='iots', verbose_name=_('Organization'))
    data = JSONField(null=True, blank=True, verbose_name=_('IoT Data'))  # Nuovo campo JSON

    class Meta:
        verbose_name = _('IoT Device')
        verbose_name_plural = _('IoT Devices')

    def __str__(self):
        return self.name



class DroneStand(models.Model):
    """
    Modello per rappresentare una stazione di ricarica per droni.
    """
    name = models.CharField(max_length=100, verbose_name=_('Drone Stand Name'))
    model = models.CharField(max_length=100, verbose_name=_('Drone Stand Model'))
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='drone_stands', verbose_name=_('Location'))
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='drone_stands', verbose_name=_('Organization'))

    class Meta:
        verbose_name = _('Drone Stand')
        verbose_name_plural = _('Drone Stands')

    def __str__(self):
        return self.name


class DroneCapture(models.Model):
    """
    Modello per rappresentare una cattura effettuata da un drone.
    """
    name = models.CharField(max_length=100, verbose_name=_('Capture Name'))
    model = models.CharField(max_length=100, verbose_name=_('Capture Model'))
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='drone_captures', verbose_name=_('Location'))
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='drone_captures', verbose_name=_('Organization'))

    class Meta:
        verbose_name = _('Drone Capture')
        verbose_name_plural = _('Drone Captures')

    def __str__(self):
        return self.name



class CustomUser(AbstractUser):
    """
    Modello utente personalizzato che estende il modello User di Django.
    """
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name=_('Role')
    )
    locations = models.ManyToManyField(Location, blank=True, related_name='users', verbose_name=_('Locations'))
    master_user = models.BooleanField(default=False, verbose_name=_('Master User'))
    change_password = models.BooleanField(default=False, verbose_name=_('Change Password'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Date'))
    modified_date = models.DateTimeField(auto_now=True, verbose_name=_('Modified Date'))
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users', verbose_name=_('Organization'))

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username
