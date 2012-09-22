from random import randrange

BLURBS = {
    'welcome': [
        'Enjoy your Journey!',
        'Roleplay to your hearts content.'
    ],
}


def blurb(style):
    choices = BLURBS[style]
    return choices[randrange(0, len(choices))]