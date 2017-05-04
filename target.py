vectors = dict()
targets = set()
from __main__ import myprint
import methods

def fadd(query):
	for uid in query:
		uid = int(uid)
		if uid in targets:
			myprint(uid, 'уже добавлен в список целей!', error=True)
		else:
			targets.add(uid)
			print('{} ({}) успешно добавлен в список целей.'.format(
				methods.names(uid), uid))

def fdelete(query):
	for uid in query:
		if uid not in targets:
			myprint(uid, 'отсутствует в списке целей!', error=True)
		else:
			targets.remove(uid)
			print(uid, 'успешно удален из списка целей.')


def flist():
	from vector import utokens, vectors
	vk = vectors[utokens[0][1]]
	i = 1
	for uid in targets:
		name = methods.names(uid, vk)
		if name:
			print('{:>2}. {} ({})'.format(i, name, uid))
		else:
			print('{:>2}. {}'.format(i, uid))
		i += 1
