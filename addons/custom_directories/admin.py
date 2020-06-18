from django.contrib import admin
from django.utils.text import slugify
from import_export import resources
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin
from import_export.fields import Field
from import_export.widgets import Widget, ForeignKeyWidget
from tendenci.apps.directories.models import Directory, Category
from tendenci.apps.files.models import File

from .utils.utils import strip_accents


class DirectoryResource(resources.ModelResource):
    cat = Field(
        default='c-street-businesses',
        attribute='cat',
        widget=ForeignKeyWidget(Category, 'slug'))
    sub_cat = Field(
        column_name='Category',
        attribute='sub_cat',
        widget=ForeignKeyWidget(Category, 'name'))

    class Meta:
        model = Directory
        import_id_fields = ('slug',)

    def skip_row(self, instance, original):
        # try:
        #     Category.objects.filter(name=instance["Category"])
        # except:
        #     return True

        return super(DirectoryResource, self).skip_row(instance, original)

    def before_import_row(self, row, row_number=None, **kwargs):
        # Avoiding a KeyError.
        row.update({"tags": ""})
        
        tag_map = {
            "Dining": "food",
            "Hot Drinks": "hot-drinks",
            "Hard Drinks": "alcohol",
            "Shopping": "retail",
            "Party": "parties",
            "Lodging": "lodging",
            "Activities": "things-to-do"
        }

        name = {
            "first_name": "",
            "last_name": ""
        }
        contact_name = ""
        try:
            contact_name = row["Contact"].split(',')[0]
            name["first_name"] = contact_name.split()[0]
            name["last_name"] = contact_name.split()[1]
        except:
            pass

        row.update(name)

        row.update({
            "headline": row["Name"],
            "slug": slugify(row["Name"]),
            "address": row["Address"],
            "city": "Springfield",
            "state": "MO",
            "zip_code": "65803",
            "country": "United States of America",
            "phone": row["Phone"],
            "email": row["Email"],
            "website": row["Website"],
            "facebook": row["Facebook"],
            "twitter": row["Twitter"],
            "instagram": row["Instagram"],
            "tripadvisor": row["TripAdvisor"],
        })

        # Need to figure out how to not override old fields for this one.
        # logo_default = File.objects.filter(tags__icontains="generic").order_by('?').first()

        row.update({
            "creator": 3,
            "creator_username": "import_bot"
        })

        # Run through the tag-appropriate columns and add them.
        for k, v in row.items():
            if (k in tag_map) & (v == '1'):
                row.update({"tags": row["tags"] + ", %s" % tag_map[k]})
        

class DirectoryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('headline', 'sub_cat', 'address')
    list_filter = ['headline', 'sub_cat']
    resource_class = DirectoryResource

admin.site.register(Directory, DirectoryAdmin)