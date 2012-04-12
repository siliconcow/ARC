from django import forms
from django.views.generic import CreateView
from django.forms import ModelForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from ajax_select.fields import AutoCompleteField
from arc.models import *

class SearchForm(forms.Form):

    q = AutoCompleteField(
            'ace',
            required=True,
            help_text="Autocomplete will suggest ArbitraryRepeatableCommands you may use. <b>Try 'i sean connery' </b>",
            label='',
            attrs={'class': 'search-query span6', 'placeholder': 'Search ARCS'}
            )

class AceForm(ModelForm):
    class Meta:
        model = Ace

class Flash(object):
    message=""
    level="info"

    def __init__(self, message, level):
        self.message=message
        self.level=level 

    def __str__(self):
        return self.message

def home(request):
    
    ctx = {}
    if request.POST:
        form=AceForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            command = form.cleaned_data['command']
            target = form.cleaned_data['target']
            type = form.cleaned_data['type']

            new_ace= Ace(name=name, command=command, target=target, type=type)
            new_ace.save()
            ctx['arc_added']=new_ace
        ctx['form_add']=form

    elif request.GET.get('q') is not None and len(request.GET.get('q').split()) > 0:
        obj = request.GET.get('q').split()
        reqstr = '%s' % ' '.join(map(str,obj[1:]))
        ace = Ace.objects.filter(command=obj[0])
        if ace:
            return redirect(ace.get().target.replace('${args}', reqstr))  
        else:
            ctx['flash']=Flash(message="Come on now, that isn't a valid ARC. Please try again.", level="error")
    elif request.GET.get('q') is not None:
        ctx['flash']=Flash(message="Begin typing to search for ARCs.  Try creating your own ARCs!", level="info")
    initial = {'q':"Search ARCS"}
    form = SearchForm()
    ctx['form'] = form
    if 'form_add' not in ctx:
        ctx['form_add'] = AceForm
    ctx['arcs'] = Ace.objects.all()
    return render_to_response('home.html',ctx,context_instance=RequestContext(request))
