from django.conf import settings
from django.db import models

from webdnd.player.models.abstract import AbstractPlayerModel
from random import randint
import re


class Roll(AbstractPlayerModel):
    '''
    ROUGH OUTLINE/ Thoughts


    What we should be able to encode....
    3d4 * (2d6 + 12) + (1.5 * str)
        1      2


    id | rolls | dice
    ---+-------+------
    1  |  3    |  d4
    2  |  2    |  d6


    id | symbol | roll | type | roll | type
    1  | *      | 1    |  die |  2   |  roll
    2  | +      | 3    | roll |  4   | roll
    3  | +      | 2    |  die |  12  |  num
    4  | *      | 1.5  | num | 'str'| attr

    floats? ....


    Attr: object that subclasses a BaseAttr
        just implements an interface?
        thus we could have it do the wierd calculations
        Just pass in the char sheet

        e.g. str modifier
        STORES: int multiplier val (default 1)
        calc:   mult * char.str

        thus, the model would need the following
        > storage of what func we use (which points to a model method)
        > storage of args (M2M? or limited number?)


    IDEA 2:
    parse a string, storing a compiled lambda function in the db
    then you eval it once saving the result into memory (as a property)

    we could then see whats used often (or even if its worth changing)
    and change it to a model based schema
    Thus we just need to create an interface
    '''

    # For now just create a single die with a mod (+n)

    num = models.IntegerField(blank=False, null=False)
    die = models.IntegerField(blank=False, null=False)

    STRING_RE = re.compile(r'(?P<num>[0-9]+)d(?P<die>[0-9]+)')

    def __unicode__(self):
        return '%(num)ud%(die)u' % {
            'num': self.num,
            'die': self.die,
        }

    @staticmethod
    def from_str(string):
        '''
        creates a Roll object based on the given string
        '''
        search = Roll.STRING_RE.match(string)
        if (search):
            num = search.group('num')
            die = search.group('die')

            return Roll(num=num, die=die)
        else:
            return False

    def format(self, character):
        '''
        Formats the roll into a string, turning all attributes into actual
        values.
        '''
        return unicode(self)

    def roll(self, character=None):
        return reduce(lambda a, b: a + b, [
            self.random() for n in range(int(self.num))
        ])

    def random(self):
        return randint(1, int(self.die))


ROLLABLE_RE = re.compile(
    '((?P<dice>[0-9]+d[0-9]+)'
        + '(?P<bonus> *'  # Modifier flag (use it as a boolean)
            + '(?P<symbol>[+-])'
            + ' *(?P<mod>[0-9]+)'
        + ')?'  # Make the bonus group optional
    + ')'
)

def roll_text(string):
    for orig in ROLLABLE_RE.findall(string):
        replace = Roll.from_str(orig[1])

        if orig[2]:
            num = int(orig[4])
            if orig[3] == '-':
                num = -1 * num
        else:
            num = 0

        if replace:
            formatted = '%(orig)s [%(roll)s]' % {
                'orig': orig[0],
                'roll': replace.roll() + num,
            }

            string = string.replace(orig[0], formatted, 1)

    return string



