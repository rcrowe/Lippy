"""
Makes use of code by Konstantin Lepa <konstantin.lepa@gmail.com>
"""

import os

__ALL__ = [ 'colored' ]

ATTRIBUTES = dict(
        list(zip([
            'bold',
            'dark',
            '',
            'underline',
            'blink',
            '',
            'reverse',
            'concealed'
            ],
            list(range(1, 9))
            ))
        )
del ATTRIBUTES['']

HIGHLIGHTS = dict(
        list(zip([
            'on_grey',
            'on_red',
            'on_green',
            'on_yellow',
            'on_blue',
            'on_magenta',
            'on_cyan',
            'on_white'
            ],
            list(range(40, 48))
            ))
        )

COLORS = dict(
        list(zip([
            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
            ],
            list(range(30, 38))
            ))
        )

RESET = '\033[0m'

__ALL__ = [ 'colored' ]


ATTRIBUTES = dict(
        list(zip([
            'bold',
            'dark',
            '',
            'underline',
            'blink',
            '',
            'reverse',
            'concealed'
            ],
            list(range(1, 9))
            ))
        )
del ATTRIBUTES['']


HIGHLIGHTS = dict(
        list(zip([
            'on_grey',
            'on_red',
            'on_green',
            'on_yellow',
            'on_blue',
            'on_magenta',
            'on_cyan',
            'on_white'
            ],
            list(range(40, 48))
            ))
        )


COLORS = dict(
        list(zip([
            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
            ],
            list(range(30, 38))
            ))
        )


RESET = '\033[0m'


def colored(text, color=None, on_color=None, attrs=None):

    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'
        if color is not None:
            text = fmt_str % (COLORS[color], text)

        if on_color is not None:
            text = fmt_str % (HIGHLIGHTS[on_color], text)

        if attrs is not None:
            for attr in attrs:
                text = fmt_str % (ATTRIBUTES[attr], text)

        text += RESET
    return text
    

def output(level, level_str, client_address):

    if level == 1:
         print(colored("\n%s - %s\n" % (level_str, client_address), 'white', 'on_cyan'))
    elif level == 2:
         print(colored("\n%s - %s\n" % (level_str, client_address), 'white', 'on_blue'))
    elif level == 3:
         print(colored("\n%s - %s\n" % (level_str, client_address), 'white', 'on_yellow'))
    elif level == 4:
         print(colored("\n%s - %s\n" % (level_str, client_address), 'white', 'on_red'))
    elif level == 5:
         print(colored("\n%s - %s\n" % (level_str, client_address), 'white', 'on_red', attrs=['underline']))

