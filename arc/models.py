from django.db import models


class Ace(models.Model):
    ACETYPES = ( ('R', 'Redirect'),)

    """ an actual singular human being """
    name = models.CharField(blank=False, max_length=100)
    type = models.CharField(blank=False, max_length=1, choices=ACETYPES)
    command = models.CharField(blank=False, max_length=100)
    target = models.CharField(blank=False, max_length=100)
  

    def __unicode__(self):
        return "%s (%s): %s" % (self.command, self.name, self.target)
