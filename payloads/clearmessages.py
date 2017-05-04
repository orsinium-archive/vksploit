"""Удаляет те сообщения, которые содержат хотя бы одно слово из списка"""

varlist = {
	'words': ['оружие', 'наркотики', 'героин', 'суицид'],
	'only_targets': 0,
	'first_form': 0
	}
descr = {
	'var1': 'descr1',
	'var2': 'descr2'
	}

def start():
	from __main__ import myprint, vk_request
	from target import targets, vectors
	from vector import vectors as vectors_info
	import methods
	
	if varlist['first_form']:
		import pymorphy2
			
	
	if type(varlist['words']) is str:
		varlist['words'] = {varlist['words']}
	else:
		varlist['words'] = set(varlist['words'])
	
	for target_id in targets:
		vector_id, lvl = vectors[target_id]
		vector_obj = vectors_info[vector_id]
		
		msgs = #!
		if not msgs:
			continue
		for msg in msgs:
			if varlist['first_form']:
				words = []
				for word in msg.split():
					words.extend(morph.normal_forms(word))
			else:
				words = msg.lower().split()
			words = set(words)
			
			if words & varlist['words']:
				if len(msg) > 80:
					print(msg[:79]+'…')
				else:
					print(msg)
				
				#del
