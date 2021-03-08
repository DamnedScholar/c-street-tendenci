from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey, TreeManyToManyField


class Category(MPTTModel):
    """
    Hierarchical category data for the directory.
    """

    name = models.CharField(max_length=50)
    parent = TreeForeignKey("self", blank=True, null=True, on_delete=models.PROTECT)


class Categorizable:
    """
    A mixin to attach categorization behavior to another model.
    """

    categories = TreeManyToManyField(Category, verbose_name=_("Categories"))
