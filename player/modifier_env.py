
# Isolates the user's code
MODIFIERS_ENV = '''
def mod(character):
    # Allowed imports that the user will has access to
    from collections import defaultdict
    # TEST: checking to see what is visible in this scope
    print locals()

    if (%(cond)s):
%(mod)s
'''
# TODO indent multiline codes


def modifier(modifier, default):
    mod = None
    try:
        exec(MODIFIERS_ENV % {
            'mod': map(lambda l: ' ' * 8 + l, modifier.modifier.split('\n')),
            'cond': modifier.condition if modifier.condition else 'True',
        })
        return mod
    except BaseException as err:
        # TODO better error handling
        print err
        return default
