from django.db import models


class SubscriptionLog (models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

# TODO: Proofread all of this once I have Internet to read the docs.
class ViewCountTarget (models.Model):
    target = models.URLField(verbose_name='Target Page')
    name = models.CharField(max_length=100)
    views = models.IntegerField()

class ViewCountLog (models.Model):
    target = models.ForeignKey('ViewCountTarget', on_delete=None)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        target = ViewCountTarget.objects.get_or_create(
            target=kwargs['url']
        )

        super().save(target=target, *args, **kwargs)  # Call the "real" save() method.
