from typing import Union
from django.db import models
from django.contrib.auth.models import AbstractUser
from admin_app.models import SuperAdmin
from organisations_app.models import OrganisationAdmin, Organisation


def get_user_entity_instance(user:AbstractUser, entity:models.Model) -> Union[models.Model, None]:
    ''' Get the entity instance for the user.

        If the user is not a member of the entity, return None.

    '''

    try:
        return entity.objects.get(user=user)
    except entity.DoesNotExist:
        return None
    

def user_is_in_entity(user:AbstractUser, entity:list[models.Model]) -> bool:
    ''' Check if the user is a member of any of the  given entities.

    '''

    for e in entity:
        if get_user_entity_instance(user, e):
            return True
    
    return False


def user_is_staff_of_organization(user:AbstractUser, organization:Organisation) -> bool:
    ''' Check if the user is a staff member of the organization.
        if the user is a staff member of the organization, return True.
        if user  is a super admin return True.

    '''
    if user_is_in_entity(user, [SuperAdmin]):
        return True
    
    org_admin = get_user_entity_instance(user, OrganisationAdmin)

    if org_admin and org_admin.organisation == organization:
        return True
    
    return False
    

