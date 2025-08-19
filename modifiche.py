from django.contrib.auth import get_user_model
from .models import CustomUser  # Assicurati che il percorso di import sia corretto


def get_objects_list(user):
    """
    Verifica i permessi dell'utente per mostrare solo le tab che l'utente può vedere e/o modificare.

    Args:
        user: L'oggetto User per cui verificare i permessi.

    Returns:
        list: Una lista di dizionari, dove ogni dizionario rappresenta un oggetto/tab da visualizzare.
              Ogni dizionario contiene 'name' e 'icon'.
    """
    objects_list = [
        {
            'name': 'Locations',
            'icon': 'ri-map-pin-line',
        },
        {
            'name': 'Iot',  # Corretto da 'Sensors' a 'Iot' per coerenza con il modello
            'icon': 'ri-sensor-line',
        },
        {
            'name': 'Drones',
            'icon': 'ri-drone-line',
        },
        {
            'name': 'DroneStand',
            'icon': 'ri-charging-pile-line'
        },
        {
            'name': 'DroneCapture',
            'icon': 'ri-camera-line'
        },
        {
            'name': 'Settings',
            'icon': 'ri-settings-line',
        },
    ]

    if user.master_user:
        return objects_list
    else:
        new_obj_list = []
        # Ottieni i permessi dell'utente attraverso il ruolo, come nel tuo codice
        user_permissions = CustomUser.objects.get(id=user.id).role.permissions.all()  # Corretto l'accesso a role
        # Ottieni i nomi degli oggetti dai permessi
        obj_perm_name_list = user_permissions.values_list('obj', flat=True).distinct() # Aggiunto distinct()

        print(f'obj_perm_name_list: {obj_perm_name_list}')

        for item in objects_list:
            if item['name'] in obj_perm_name_list:
                new_obj_list.append(item)
        return new_obj_list
