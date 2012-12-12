
# Isolates the user's code
MODIFIERS_ENV = '''
def mod(character):
    # Allowed imports that the user will has access to
    from collections import defaultdict

    if (%(cond)s):
%(mod)s
'''
# TODO indent multiline codes


def modifier(modifier, default):
    mod = None
    try:
        code = MODIFIERS_ENV % {
            'mod': '\n'.join(map(lambda l: ' ' * 8 + l, modifier.modifier.split('\n'))),
            'cond': modifier.condition if modifier.condition else 'True',
        }
        exec(code)
        return mod
    except BaseException as err:
        # TODO better error handling
        print err
        return default
