from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

class GenderChoice(TextChoices):
        MALE = "male"
        FEMALE = "female"
        OTHERS = "others"
