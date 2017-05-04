import readline

class MyCompleter(object):  # Custom completer

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options 
                                    if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try: 
            return self.matches[state]
        except IndexError:
            return None

keywords = [
	'vector ',
	'payload ',
	'target ',
	'add ',
	'get ',
	'list ',
	'delete ',
	'info ',
	'use ',
	'set ',
	'start ',
	'help '
	]
from os import listdir
pll = listdir('payloads')
pll = [i[:-3] for i in pll if i.endswith('.py')]
keywords.extend(pll)

completer = MyCompleter(keywords)
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')

if __name__ == '__main__':
	while 1:
		i = input("Input: ")
		print("You entered", i)
		readline.add_history(i)
