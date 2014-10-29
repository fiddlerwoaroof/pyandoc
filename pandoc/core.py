import subprocess

try: from shutils import which
except ImportError: from distutils.spawn import find_executable as which

PANDOC_PATH = which('pandoc')


class Document(object):
   """A formatted document."""

   INPUT_FORMATS = (
      'native', 'markdown', 'markdown+lhs', 'rst',
      'rst+lhs', 'html', 'latex', 'latex+lhs'
   )

   OUTPUT_FORMATS = (
      'native', 'html', 'html+lhs', 's5', 'slidy',
      'docbook', 'opendocument', 'odt', 'epub',
      'latex', 'latex+lhs', 'context', 'texinfo',
      'man', 'markdown', 'markdown+lhs', 'plain',
      'rst', 'rst+lhs', 'mediawiki', 'rtf', 'html5'
   )

   SPECIAL_FORMATS = (
       ('html+mathjax', 'html', 'mathjax'),
       ('html5+mathjax', 'html5', 'mathjax'),
   )

   # TODO: Add odt, epub formats (requires file access, not stdout)

   def __init__(self):
      self._content = None
      self._format = None
      self._register_formats()

   @classmethod
   def _register_formats(cls):
      """Adds format properties."""
      for fmt in cls.OUTPUT_FORMATS:
         clean_fmt = fmt.replace('+', '_')
         setattr(cls, clean_fmt, property(
            (lambda x, fmt=fmt: cls._output(x, fmt)), # fget
            (lambda x, y, fmt=fmt: cls._input(x, y, fmt)))) # fset
      for fmt in cls.SPECIAL_FORMATS:
         clean_fmt = fmt[0].replace('+', '_')
         setattr(cls, clean_fmt, property(
            (lambda x, fmt=fmt: cls._output(x, fmt[1], fmt[2])), # fget
            (lambda x, y, fmt=fmt: cls._input(x, y, fmt[1], fmt[2])))) # fset



   def _input(self, value, format=None, modifiers=None):
      # format = format.replace('_', '+')
      self._content = value
      self._format = format
      self._modifiers = None

   def _output(self, format, modifiers=None):
      # print format
      if modifiers is None:
        cmdline = [PANDOC_PATH, '--from=%s' % self._format, '--to=%s' % format]
      else:
        cmdline = [PANDOC_PATH, '--from=%s' % self._format, '--to=%s' % format,
                   '--%s' % modifiers]

      p = subprocess.Popen(
         cmdline,
         stdin=subprocess.PIPE,
         stdout=subprocess.PIPE
      )

      return p.communicate(self._content)[0]
