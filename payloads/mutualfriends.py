"""Модуль для поиска общих друзей между заданными целями."""

varlist = {
	'depth': 3,
	'names': 1,
	}
descr = {
	'depth': 'Число рукопожатий (от 1 до 3)',
	'names': 'Выводить имена (1 - да, 0 - нет)',
	}

def start():
	from __main__ import myprint
	from target import targets
	import methods
	
	def print_rez(data, i):
		if len(data):
			myprint(i, 'рукопожатие(я):')
			for ids in data:
				if varlist['names']:
					d = ['{} ({})'.format(methods.names(uid), uid) for uid in ids]
				else:
					d = [str(uid) for uid in ids]
				myprint(' -> '.join(d))
	
	ltargets = list(targets)
	
	#1 рукожопатие
	rez = []
	for target_id in ltargets:
		fr1 = methods.friends(target_id)
		mut = fr1 & set(targets)
		if mut:
			for uid in mut:
				rez.append((target_id, uid))
	print_rez(rez, 1)
	
	#2 рукожопатия
	if varlist['depth'] > 1:
		rez = []
		for i in range(len(ltargets)-1):
			for j in range(i+1, len(ltargets)):
				fr1 = methods.friends(ltargets[i])
				fr2 = methods.friends(ltargets[j])
				mut = fr1 & fr2
				if mut:
					for uid in mut:
						if uid != ltargets[i] and uid != ltargets[j]:
							rez.append((ltargets[i], uid, ltargets[j]))
		print_rez(rez, 2)
	
	#3 рукожопатия
	if varlist['depth'] > 2:
		rez = []
		for i in range(len(ltargets)-1):
			for j in range(i+1, len(ltargets)):
				fr1 = methods.friends(ltargets[i])
				fr2 = methods.friends(ltargets[j])
				for fr in fr1:
					fr3 = methods.friends(fr)
					mut = fr2 & fr3
					if mut:
						for uid in mut:
							if uid != ltargets[i] and uid != ltargets[j] \
							and fr != ltargets[i] and fr != ltargets[j]:
								rez.append((ltargets[i], fr, uid, ltargets[j]))
		print_rez(rez, 3)
