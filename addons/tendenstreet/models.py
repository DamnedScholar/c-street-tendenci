from django.db import models


class FocusPoint (models.Model):
    # This needs to be a model with a ForeignKey or URL field that can be associated with any kind of image, but it needs to be unique so that each image can only have one FocusPoint. When the FocusPoint tag is included, it will query these models with the image's identifier. Using absolute URL is probably best, since that would allow me to incorporate images not hosted on the site.
    pass
