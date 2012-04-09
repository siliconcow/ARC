from django.db import models


class Ace(models.Model):

    """ an actual singular human being """
    name = models.CharField(blank=False, max_length=100)
    shortcut = models.CharField(blank=False, unique=True, max_length=100)
    target = models.CharField(blank=False, unique=True, max_length=255)
    command_type = models.ForeignKey('CommandType')

    def __unicode__(self):
        return "%s (%s): %s" % (self.shortcut, self.name, self.command_type)

class CommandType(models.Model):
    name = models.CharField(blank=False, unique=True, max_length=100)
    template = models.TextField()

    def __unicode__(self):
        return self.name

