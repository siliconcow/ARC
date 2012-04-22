from django.db import models


class Ace(models.Model):

    """ an actual singular human being """
    name = models.CharField(blank=False, max_length=100, help_text="The name of your ARC")
    shortcut = models.CharField(blank=False, unique=True, max_length=100, help_text="The characters used to execute your ARC")
    target = models.TextField(help_text="The string to pass to the command. <br> ${args} to use the entire query as a string <br>  ${arg0}..${argN} to use individual parameters <br>  You can also use basic python expressions with ${} or javascript. <br> ${pargs} gives you a python list of arguments, ${jargs} gives you javascript")
    command_type = models.ForeignKey('CommandType', help_text="The type of command to use")
    comment = models.TextField(blank=True, help_text="Explain how to use your ARC.  i.e Searches google with given parameters")

    def __unicode__(self):
        return "%s (%s): %s" % (self.shortcut, self.name, self.command_type)

class CommandType(models.Model):
    name = models.CharField(blank=False, unique=True, max_length=100)
    template = models.TextField(help_text="Any valid Evoque template")

    def __unicode__(self):
        return self.name

