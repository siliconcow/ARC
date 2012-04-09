"""
Evoque - managed eval-based freeform templating 
Copyright (C) 2007 Mario Ruggier <mario@ruggier.org>
Licensed under the Academic Free License version 3.0
URL: http://evoque.gizmojo.org/
------------------------------------------------------------------------------
$URL$

$begin{quoted_no_more_doc} $prefer{filters=[markdown]}

A *quoted-no-more infectious* string type is a subclass of Python's unicode 
string class and instances of such a type are known to not need any further 
quoting. It is *infectious* in the sense that when combined with
strings of other types, those strings will be first quoted.
This *infectious* behaviour may be summarized with (where `qnm` is a 
*quoted-no-more* instance and `s` is some other string instance):

    qnm + s = qnm + QNM(s)
    qnm_join([s, qnm, ...]) = QNM(s) + qnm + ...
    QNM("x %(key)s") % dict(key=s) = QNM("x ") + QNM(s)

Thus, the *quoted-no-more* pattern is a convenient way to liberally combine 
strings without having to worry about whether they are quoted or not, 
or whether they will ever be double-quoted.

The origins of the *quoted-no-more* pattern is the 
[QPY Quoted String Data Type][qpy_quoted], and it is central to Evoque --
for custom *automatic once-and-only-once quoting*, all templates need to do 
is specify a *quoted-no-more* class as the value of the 
`quoting` parameter.

Custom *quoted-no-more* classes should subbclass 
`evoque.quoted.quoted_no_more` and provide an implementation for 
the `_quote(s)` class method, whose sole responsibility 
is to quote a single unicode and return it as an instance of 
the custom *quoted-no-more* class itself. 

To explicitly quote a string or any other object, the class 
method `quote(obj)` is what should be used. 
This class method is defined by the `quoted_no_more` base class
and will internally call the `_quote(s)` method on the 
subclass -- where `s` is a unicode-ified representation of the
`obj` parameter received by `quote(obj)`.

The `evoque.quoted` package includes some sample *quoted-no-more* 
implementations, such as the ones for `xml` and `url` quoted strings.

[qpy_quoted]: http://www.mems-exchange.org/software/qpy/ "QPY Quoted String"

$end{quoted_no_more_doc}
"""

import sys
from evoque import decodeh

# Standardize on types for both py2 and py3
if sys.version < '3':
    unistr, string = unicode, basestring
    number_classes = (int, long, float)
else:
    unistr, string = str, str
    number_classes = (int, float)


class _quote_wrapper(object):
    """ Not for outside code.
    For values that are used as arguments to the % operator, this allows
    str(value) and repr(value), if called as part of the formatting, to
    produce quoted results.
    """
    
    __slots__ = ('qnm_cls', 'value',)
    
    def __init__(self, qnm_cls, value):
        self.qnm_cls = qnm_cls
        self.value = value
    
    def __str__(self):
        return self.qnm_cls.quote(self.value)
    
    def __repr__(self):
        return self.qnm_cls.quote(repr(self.value))
    
    def __getitem__(self, key):
        return self.qnm_cls._quote_wrap(self.value[key])


class quoted_no_more(unistr):
    """ instances of the quoted_no_more subclass of unistr are designated as
        needing no more quoting.
    """
    
    __slots__ = ()

    def _quote_wrap(cls, x):
        """ (x) -> either(_quote_wrapper, x)
        Not for outside code.
        Return a value v for which str(v) and repr(v) will produce quoted 
        strings, or, if x is a dict, for which str(v[key]) and repr(v[key]) 
        will produce quoted strings.
        """
        if isinstance(x, number_classes):
            return x
        else:
            return _quote_wrapper(cls, x)
    _quote_wrap = classmethod(_quote_wrap)
    
    def __new__(cls, s=None):
        """ (s:either(string, None)) """
        if s is None:
            return cls("")
        elif not isinstance(s, unistr):
            s = decodeh.decode(s)
        return unistr.__new__(cls, s)

    def __add__(self, other):
        """ (other) -> self.__class__
        """
        return self.__class__(unistr.__add__(self, self.quote(other)))

    def __radd__(self, other):
        """ (other:str) -> self.__class__
        """
        if isinstance(other, string):
            return self.__class__(unistr.__add__(self.quote(other), self))
        else:
            return NotImplemented

    def __mul__(self, other):
        """ (other) -> self.__class__
        """
        return self.__class__(unistr.__mul__(self, other))

    def __rmul__(self, other):
        """ (other) -> url
        """
        return self.__class__(unistr.__mul__(self, other))

    def __mod__(self, other):
        """ (other) -> self.__class__
        """
        if isinstance(other, tuple):
            target = tuple(self._quote_wrap(item) for item in other)
        else:
            target = self._quote_wrap(other)
        return self.__class__(unistr.__mod__(self, target))

    def join(self, items):
        """ (items:tuple(string)) -> self.__class__
        Generic form of str.join.
        """
        return self.__class__(unistr.join(
                self, (self.quote(item) for item in items)))
    
    def quote(cls, x):
        """ (x:anything) -> cls
        
        When the x argument is an own_type instance, it is just returned 
        immediately, without any changes. 
        When it is None, an empty cls instance is returned. 
        All other arguments are converted to unicode strings and then 
        quoted to produce an instance of cls.
        """
        if isinstance(x, cls):
            return x
        if x is None:
            return cls()
        if type(x) is unistr:
            s = x
        elif isinstance(x, string):
            s = decodeh.decode(x)
        else:
            s = unistr(x)
        return cls._quote(s)
    quote = classmethod(quote)
    
    def _quote(cls, s):
        """(s:str) -> cls
        Quotes the unicode string s, and returns an instance of cls.
        What sub-slasses should override.
        """
        return s
    _quote = classmethod(_quote)
    

# generic join
quoted_no_more_join = quoted_no_more().join

__all__ = ["quoted_no_more", "quoted_no_more_join"]
