import sys
# Bash colors:
# http://misc.flogisoft.com/bash/tip_colors_and_formatting

ANSI_FORMAT = '\x1b[%sm'

FORMATTINGS = {
    'bold': 1,
    'dim': 2,
    'underline': 4,
    'blink': 5,
    'reverse': 7,
    'hidden': 8,
}

FG_COLORS = {
    'default': 39,
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'light_gray': 37,
    'dark_gray': 90,
    'light_red': 91,
    'light_green': 92,
    'light_yellow': 93,
    'light_blue': 94,
    'light_magenta': 95,
    'light_cyan': 96,
    'white': 97,
}

BG_COLORS = {
    'default': 49,
    'black': 40,
    'red': 41,
    'green': 42,
    'yellow': 43,
    'blue': 44,
    'magenta': 45,
    'cyan': 46,
    'light_gray': 47,
    'dark_gray': 100,
    'light_red': 101,
    'light_green': 102,
    'light_yellow': 103,
    'light_blue': 104,
    'light_magenta': 105,
    'light_cyan': 106,
    'white': 107,
}


FORMATTER_COLORS = {'reset': ANSI_FORMAT % 0}

for k, v in FG_COLORS.items():
    FORMATTER_COLORS[k] = ANSI_FORMAT % v
    FORMATTER_COLORS['/%s' % k] = ANSI_FORMAT % FG_COLORS['default']

for k, v in BG_COLORS.items():
    FORMATTER_COLORS['on_%s' % k] = ANSI_FORMAT % v
    FORMATTER_COLORS['/on_%s' % k] = ANSI_FORMAT % BG_COLORS['default']

for k, v in FORMATTINGS.items():
    FORMATTER_COLORS[k] = ANSI_FORMAT % v
    FORMATTER_COLORS['/%s' % k] = ANSI_FORMAT % (v + 20)

NO_TTY_FORMATTER_COLORS = {}
for k, v in FORMATTER_COLORS.items():
    NO_TTY_FORMATTER_COLORS[k] = ''


def formatter(s):
    if sys.stdout.isatty():
        return '%s%s' % (s.format(**FORMATTER_COLORS), (ANSI_FORMAT % 0))
    # Not a tty, we remove the formatting
    return s.format(**NO_TTY_FORMATTER_COLORS)


def parse_attr(attr):
    formatting = None
    fgcolor = None
    bgcolor = None
    bg = False
    for name in attr.split('_'):
        if bg:
            if name not in BG_COLORS:
                raise Exception('Bad background color: %s' % name)
            bgcolor = BG_COLORS[name]
            bg = False
        elif name in FORMATTINGS:
            formatting = FORMATTINGS[name]
        elif name in FG_COLORS:
            fgcolor = FG_COLORS[name]
        elif name == 'on':
            bg = True
        else:
            raise Exception('Bad attribute: %s' % name)

    return {
        'formatting': formatting,
        'fgcolor': fgcolor,
        'bgcolor': bgcolor
    }


def applycolor(text, formatting=None, bgcolor=None, fgcolor=None):
    if not sys.stdout.isatty():
        # Not a tty, we don't apply any rendering
        return text
    lis = filter(bool, [formatting, bgcolor, fgcolor])
    if not lis:
        return text
    reset = ANSI_FORMAT % 0
    prefix = ANSI_FORMAT % (';'.join(map(str, lis)))
    return '%s%s%s' % (prefix, text, reset)


class ColorTerm(object):

    def __getattr__(self, attr):
        dic = parse_attr(attr)
        return lambda x: applycolor(x, **dic)
