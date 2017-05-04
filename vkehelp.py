from __main__ import myprint
from os import listdir
helplist = listdir('help')
def fmain(query):
	query = ' '.join(query)
	if query in helplist:
		f = open('help/'+query)
		print('+', '-'*80, '+', sep='')
		for i in f:
			print('|{:80}|'.format(i[:-1]))
		print('+', '-'*80, '+', sep='')
	else:
		myprint('help for', query, 'not found!', error=True)
