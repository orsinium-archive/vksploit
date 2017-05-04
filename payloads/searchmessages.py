"""Модуль для поиска сообщений по заданному шаблону"""

varlist = {
	'query': 'люблю',
	'count': 100
	}
descr = {
	'query': 'Поисковый запрос',
	'count': 'Максимальное число результатов (от 1 до 100)'
	}

def start():
	from __main__ import myprint, vk_request
	from target import targets, vectors
	from vector import vectors as vectors_info
	import methods
	from time import gmtime, strftime
	
	for target_id in targets:
		vector_id, lvl = vectors[target_id]
		vector_obj = vectors_info[vector_id]
		if lvl == 1:
			myprint('Цель', target_id, 'не может быть атакована! Необходим вектор I уровня.')
		else:
			rez = vk_request(vector_obj, 'messages.search', 
				{'q': varlist['query'], 'count': varlist['count']})
			if not rez:
				myprint('Сообщение не найдено!')
			else:
				rez = rez['items']
				for info in rez:
					myprint()
					myprint('{} ({}):'.format(methods.names(info['user_id']), info['user_id']))
					myprint(info['body'])
					myprint(strftime('[%d.%m.%Y %H:%M]', gmtime(info['date'])))
