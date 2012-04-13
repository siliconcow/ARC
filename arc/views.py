from django import forms
from django.forms.models import inlineformset_factory
from django.views.generic import CreateView
from django.forms import ModelForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from ajax_select.fields import AutoCompleteField
from arc.models import *
from arc.quoted import quoted_no_more
from evoque.domain import Domain
import os


class SearchForm(forms.Form):

    q = AutoCompleteField(
            'ace',
            required=True,
            help_text="Autocomplete will suggest ArbitraryRepeatableshortcuts you may use. <b>Try 'i sean connery' </b>",
            label='',
            attrs={'class': 'well search-query span6', 'placeholder': 'Search ARCS'}
            )


class AceForm(ModelForm):
  class Meta:
     model = Ace

class Flash(object):
    message=""
    level="info"

    def __init__(self, message, level=None):
        self.message=message
        self.level=level 

    def __str__(self):
        return self.message

def home(request):
    
    ctx = {}
    if request.POST:
        form=AceForm(request.POST)
        if form.is_valid():
            success=True #ghetto flow control 
            try:
                testargs={'5','5'}
                domain.set_template("test", src=form.cleaned_data['target'], data=testargs, from_string=True, quoting='str')
                compiledTmpl=domain.get_template('test')
            except:
                ctx['flash']=Flash(message="Sorry, we couldn't add that ARC. The Target provided couldn't be compiled.  See http://evoque.gizmojo.org/syntax/ for details.", level="error")
                success=False
            if success:
                name = form.cleaned_data['name']
                shortcut = form.cleaned_data['shortcut']
                target = form.cleaned_data['target']
                command_type = form.cleaned_data['command_type']

                new_ace= Ace(name=name, shortcut=shortcut, target=target, command_type=command_type)
                new_ace.save()
                ctx['arc_added']=new_ace
        ctx['form_add']=form

    elif request.GET.get('q') is not None and len(request.GET.get('q').split()) > 0:
        q = request.GET.get('q').split()
        reqstr = '%s' % ' '.join(map(str,q[1:]))
        ace = Ace.objects.filter(shortcut=q[0])
        if ace:
            domain = Domain(os.path.abspath("."), restricted=True)
            arglist = map(lambda x: 'arg'+x.__str__(), xrange(0, len(q)))
            args = dict(zip(arglist, q))
            args['args']=reqstr
            target = ace.get().target
            domain.set_template("target", src=target, data=args, from_string=True, quoting='str')
            compiledTargetTmpl=domain.get_template("target")
            result=compiledTargetTmpl.evoque()
            template = ace.get().command_type.template
            args['ace'] = result
            domain.set_template("template", src=template, data=args, quoting=quoted_no_more, raw=False, from_string=True)
            compiledTmpl=domain.get_template('template')
            ctx['template'] = compiledTmpl.evoque()
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
