
'''
OpenAI Synthetic Language Task:

C. Building Blocks for Synthetic Tasks
We describe the 13 building blocks used to create synthetic tasks for evaluating model performance as a function of docstring complexity. Each building block is specified by a line of text and a line of code:

'''
from collections import namedtuple

Element = namedtuple('Element', ['description', 'rule'])

synthetic_grammar = dict(
    remove_all=Element(
        "remove all instances of the letter e from the string"
        lambda s : s.replace("e", "")),
    replace_spaces=Element(
        "replace all spaces with exclamation points in the string",
        lambda s : s.replace(" ", "!")),
    lower=Element(
        "convert the string s to lowercase",
        lambda s : s.lower()),
    remove_first_two_chars=Element(
        "remove the first and last two characters of the string",
        lambda s : s[2:-2]),
    remove_vowels=Element(
        "removes all vowels from the string",
        lambda s : "".join(char for char in s if char not in "aeiouAEIOU")),
    remove_every_third=Element(
        "remove every third character from the string",
        lambda s : "".join(char for i, char in enumerate(s) if i % 3 != 0)),
    drop_last_half=Element(
        "drop the last half of the string, as computed by characters",
        lambda s : s[: len(s) // 2]),
    replace_spaces_with_triple_space=Element(
        "replace spaces with triple spaces",
        lambda s : s.replace(" ", "   ")),
    reverse_word_order=Element(
        "reverse the order of words in the string",
        lambda s : " ".join(s.split()[::-1])),
    drop_first_half_by_words=Element(
        "drop the first half of the string, as computed by number of words",
        lambda s : " ".join(s.split()[len(s.split ()) // 2 :])),
    add_apples_after_each_words=Element(
        "add the word apples after every word in the string",
        lambda s : " ".join(word + " apples" for word in s.split())),
    every_other_uppercase=Element(
        "make every other character in the string uppercase",
        lambda s : "".join(char.upper() if i % 2 == 0 else char for i, char in enumerate(s))),
    delete_punctuation=Element(
        "delete all excamation points, question marks, and periods from the string",
        lambda s : "".join([x for x in s if x not in ".!?"])))

'''
This synthetic task is arbitrary, and a lot of the operators could be generalized into a grammar

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
