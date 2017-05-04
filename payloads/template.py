"""Descr"""

varlist = {
	'var1': 'val1',
	'var2': 'val2'
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
	
	for target_id in targets:
		vector_id, lvl = vectors[target_id]
		vector_obj = vectors_info[vector_id]
		
