'''
Consider the regex-like string language:
    abc (terminals)
    3a    = aaa    # Repetition
    3(ab) = ababab # Grouping

    33a = aaaaaaaaa ?

    Rules:
        expr      = group | repeat | primitive
        group     = ( inner )
        inner     = expr  | expr expr
        repeat    = num expr
        num       = 2 | 3 | 4 ..
        primitive = a | b | c ..

    Example:
        a, b, c
        aa, ab, ac, ba, bb, bc, ca, cb, cc, 2a, 3a, 2b, 3b, 2c, 3c
        2(ab) a2(b) # Rules can be inserted into middle, so AST required
        # However a2b will come from finding 2b and then a2b...
'''

from collections import namedtuple

StringTree = namedtuple('StringTree', ['content', 'name', 'child'])

class StringLanguage:
    def __init__(self):
        self.terminals = 'abc'
        self.nums      = [2, 3, 4]
        self.rules = [self.repeat, self.group]

    def repeat(self, expr):
        for num in self.nums:
            yield StringTree(num, 'repeat', expr)

    def group(self, expr):
        for term in self.terminals:
            yield StringTree(term, 'group', expr)

    def initial(self):
        for term in self.terminals:
            yield StringTree(term, 'terminal', None)

    def grow(self, programs):
        for program in programs:
            yield program
            for rule in self.rules:
                yield from rule(program)

    def interpret(self, node):
        match node.name:
            case 'terminal':
                return node.content
            case 'repeat':
                return node.content * self.interpret(node.child)
            case 'group':
                return node.content + self.interpret(node.child)

    def render(self, node):
        match node.name:
            case 'terminal':
                return node.content
            case 'repeat':
                return f'{node.content}({self.render(node.child)})'
            case 'group':
                return f'{node.content}({self.render(node.child)})'

def filter_observationally_equivalent(language, programs, inputs):
    seen = set()
    for program in programs:
        output = language.interpret(program)
        if output not in seen:
            seen.add(output)
            yield program

def bottom_up_explicit(language, inputs, outputs):
    programs = list(language.initial())
    while True:
        programs.extend(list(language.grow(programs)))
        programs = list(filter_observationally_equivalent(language, programs, inputs))
        for program in programs:
            if language.interpret(program) == outputs:
                return program

def main():
    language = StringLanguage()
    # programs = list(language.initial())
    # for i in range(3):
    #     for program in programs:
    #         print(language.render(program))
    #     programs.extend(list(language.grow(programs)))
    # target = 'aaa'
    target = 'ababab'
    result = bottom_up_explicit(language, '', target)
    print(language.render(result), ' -> ', target)

if __name__ == '__main__':
    main()
