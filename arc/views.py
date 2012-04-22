from django import forms
from django.forms.models import inlineformset_factory
from django.views.generic import CreateView
from django.forms import ModelForm
from django.utils.html import escape
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
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
    def __init__(self, message, level="info"):
        self.message=message
        self.level=level 

    def __str__(self):
        return self.message

def escapeTargets(arcs):
    for arc in arcs:
        arc.escaped_target=escape(escape(arc.target))  ##this is some nonesense required because you have to double-escape code in HTML attribtues.
        arc.escaped_command=escape(escape(arc.command_type.template))  ##this is some nonesense required because you have to double-escape code in HTML attribtues.
        arc.escaped_comment=escape(escape(arc.comment))  ##this is some nonesense required because you have to double-escape code in HTML attribtues.
    return arcs

#@login_required
def home(request):

    ctx = {}
    domain = Domain(os.path.abspath("."), restricted=True) #marginal template security, people can still DOS us.   Don't tell anyone.
    if request.POST:
        form=AceForm(request.POST)
        if form.is_valid():
            success=True 
            try:
                testargs={'args': 'test'}
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
        else:
            ctx['flash']=Flash(message="Sorry, we couldn't add that ARC. Please try again", level='alert-block')
        ctx['form_add']=form

    elif request.GET.get('q') is not None and len(request.GET.get('q').split()) > 0:
        q = request.GET.get('q').lower().split()
        reqstr = '%s' % ' '.join(map(str,q[1:]))
        ace = Ace.objects.filter(shortcut=q[0])
        if ace:
            arglist = map(lambda x: 'arg'+x.__str__(), xrange(0, len(q))) #creating arglist=['arg0','arg1','argN']
            args = dict(zip(arglist, q)) #creating args={'arg0': 'some arguement', etc}
            if len(args) is 1:  #so evoque doesn't die on empty arguments
                args["arg1"] = None
            args['jargs']="var %s = ['%s']" % ('args', "','".join(q[1:]))  #args in javascript
            args['pargs']=q #pythonic args
            args['args']=reqstr #args in a single string
            args['arc']=ace.get().name
            target = ace.get().target
            domain.set_template("target", src=target, data=args, from_string=True, quoting='str')
            compiledTargetTmpl=domain.get_template("target")
            result=compiledTargetTmpl.evoque()
            if ace.get().command_type.name == u'redirect':
                return redirect(result) 
            template = ace.get().command_type.template
            args['ace'] = result
            domain.set_template("template", src=template, data=args, quoting='str', raw=False, from_string=True)
            compiledTmpl=domain.get_template('template')
            ctx['template'] = compiledTmpl.evoque()
        else:
            gotoGoogle='/?q=g+%s' % ''.join(map(str,q))
            return redirect(gotoGoogle) # not found, it's google's problem now (feature parity with pre-ACE)
    elif request.GET.get('q') is not None:
        ctx['flash']=Flash(message="Begin typing to search for ARCs.  Try creating your own ARCs!", level="info")
    initial = {'q':"Search ARCS"}
    form = SearchForm()
    ctx['form'] = form
    if 'form_add' not in ctx:
        ctx['form_add'] = AceForm
    ctx['arcs'] = escapeTargets(Ace.objects.all())
    return render_to_response('home.html',ctx,context_instance=RequestContext(request))
