grammar = {
    # 'program': ('<sp og>', '¶','{','¶', '<sp op1>', '}'),# 14 konflicts
    'program': ('<sp og>', '¶','{', '<sp op1>', '}'),
    'sp og': (
        ('<og>', '¶'),
        ('<sp og>', '<og>', '¶')
    ),
    'og':('<type>','<sp zm>'),
    'type':(
        ('int',),
        ('float',),
        ('label',)
    ),
    'sp zm':(
        ('idn',),
        ('idn',',','<sp zm>')
    ),
    'sp op1':('<sp op>',),
    'sp op':(
        ('<sp op>','<op>','¶'),
        ('<op>','¶')
    ),
    # 'op1':('<op>',),
    'op':(
        ('<input>',),
        ('<output>',),
        ('<prisv>',),
        ('<loop>',),
        ('<cond op>',),
        ('<label call>',),
        ('lab',':')
    ),
    'input':(
        ('cin','>>','idn'),
        ('<input>','>>','idn')
    ),
    'output':(
        ('cout','<<','idn'),
        ('<output>','<<','idn')
    ),
    'prisv':(
        ('idn','=','<expr1>'),
        ('idn','=','<tern op>')
    ),
    'expr1':('<expr>',),
    'loop':('for','idn','=','<expr1>','by','<expr1>','while','<cond>','do','<op>'),
    'cond op':('if','<cond>','then','<label call>'),
    'label call':('goto','lab'),
    'tern op':('<cond>','?','<expr1>',':','<expr1>'),
    'cond':('<expr>','<znak vidn>','<expr1>'),
    'znak vidn':('<','>','>=','<=','==','!='),
    'expr':(
        ('<expr>','+','<term1>'),
        ('<expr>','-','<term1>'),
        ('<term>',)
    ),
    'term1':('<term>',),
    'term':(
        ('<term>','*','<factor>'),
        ('<term>','/','<factor>'),
        ('<factor>',)
    ),
    'factor':(
        ('idn',),
        ('constant',),
        ('(','<expr1>',')')
    )
}