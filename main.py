#!/usr/bin/python3

result = []
def myprint(*argv, sep=' ', end='\n', error=False):
	if error:
		print('\x1B[31m[!]', end=' ')
	else:
		text = sep.join([str(i) for i in argv])+end
		result.append(text)
	print(*argv, sep=sep, end='\x1B[0m'+end)


from time import sleep
def vk_request(vk, method, params):
	for i in (1,2,3,0):
		try:
			rez = vk(method, **params)
		except Exception as e:
			exc = e
			sleep(i)
		else:
			return rez
	if not str(exc).startswith('15.'): #if not "user deactivated"
		myprint(exc, error=True)
	return False


import readline
import inputer

import vkehelp
import target
import vector
import exploit
import payload

from sys import argv
if len(argv)>1:
	fname = ' '.join(argv[1:])
	try:
		f = open(fname)
	except:
		myprint('Файл', fname, 'не найден!', error=True)
		queue = []
	else:
		queue = f.readlines()
else:
	queue = []



def main(query):
	if query[0] == 'help':
		if len(query) == 1:
			query.append('main')
		vkehelp.fmain(query[1:])
	elif query[0] == 'exit':
		print('Exit...')
		exit()
	elif len(query) == 1:
		vkehelp.fmain(query)
	
	elif query[0] == 'auto':
		try:
			f = open(' '.join(query[1:]))
		except:
			myprint('Файл не найден!', error=True)
		else:
			queue.extend(f.readlines())
	
	elif query[0] == 'vector':
		if query[1] == 'add':
			if len(query) == 2:
				vector.fadd(False)
			else:
				vector.fadd(query[2:])
		elif query[1] == 'list':
			vector.flist()
		elif query[1] == 'get':
			if len(query) == 2:
				vector.fget(list(target.targets))
			else:
				vector.fget(query[2:])
		elif query[1] == 'delete':
			if len(query) == 2:
				vector.fdelete(list(vector.vectors))
			else:
				vector.fdelete(query[2:])
		else:
			vkehelp.fmain(query)
	
	elif query[0] == 'target':
		if query[1] == 'list':
			target.flist()
		elif query[1] == 'delete':
			if len(query) == 2:
				target.fdelete(list(target.targets))
			else:
				target.fdelete(query[2:])
		elif len(query) == 2:
			vkehelp.fmain(query)
		elif query[1] == 'add':
			target.fadd(query[2:])
		else:
			vkehelp.fmain([query[0]])
	
	elif query[0] == 'payload':
		if query[1] == 'list':
			payload.flist()
		elif query[1] == 'start':
			payload.fstart()
		elif len(query) == 2:
			vkehelp.fmain(query)
		elif query[1] == 'info':
			payload.finfo(query[2:])
		elif query[1] == 'use':
			payload.fuse(query[2:])
		elif query[1] == 'set':
			payload.fset(*query[2:])
		else:
			vkehelp.fmain([query[0]])
	
	elif query[0] == 'save':
		fname = ' '.join(query[1:])
		try:
			f = open(fname, 'w')
		except Exception as e:
			myprint(e, error=True)
		else:
			f.write(''.join(result))
			f.close()
			print('Данные успешно сохранены!')
	else:
		myprint('Команда не найдена!', error=True)

if __name__ == '__main__':
	try:
		while 1:
			if queue:
				query = queue.pop(0).replace('\n', '')
				print('\x1B[32m>', query, '\x1B[0m')
			else:
				query = input('\x1B[32m> ')
				print('\x1B[0m', end='')
			if not query:
				continue
			readline.add_history(query)
			query = query.split()
			main(query)
	except (EOFError, KeyboardInterrupt):
		print('\x1B[0m\nExit...')
	#except Exception as e:
	#	myprint(e, error=True)
	finally:
		if vector.utokens:
			from pickle import dump
			with open('vectors', 'wb') as f:
				dump(vector.utokens, f)
