from django.db.models import Q
from django.utils.html import escape
from arc.models import *
from ajax_select import LookupChannel


class AceLookup(LookupChannel):

    model = Ace

    def get_query(self,q,request):
        self.q=q.replace(' ', '')
        return Ace.objects.filter(Q(command__icontains=self.q) | Q(command__istartswith=self.q) | Q(name__istartswith=self.q)).order_by('command')

    def get_result(self,obj):
        u""" result is the simple text that is the completion of what the Ace typed """
        return obj.command

    def format_match(self,obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        boldq="<b>%s</b>" % self.q
        return u"<div><i>%s</i></div>" % (escape(obj).replace(self.q, boldq))

    def can_add(self,user,argmodel):
        return True

    def check_auth(self, request):
        pass
