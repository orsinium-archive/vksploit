"""Модуль для поиска лайкнутых постов в группах из списка групп пользователя"""

varlist = {
	'links': ''
	}
descr = {
	'links': 'Если не указано, ищет в группах пользователя'
	}

from __main__ import myprint, vk_request
def print_post(post):
	post['text'] = post['text'].replace('\n', ' ')
	if len(post['text']) > 78:
		post['text'] = post['text'][:77]+'…'
	myprint('   ', post['text'])
	myprint('    https://vk.com/wall', post['owner_id'],'_', post['id'], sep='')

def my_iter(vector_obj, target_id):
	if not varlist['links']:
		#сообщества юзера
		groups = vk_request(vector_obj, 'groups.get', 
			{'user_id': target_id, 'count': 1000})
		if not groups:
			myprint('  Невозможно получить список групп!', error=True)
			return
		for group in groups['items']:
			yield '-'+(group.replace('-', ''))
	else:
		#список ссылок
		for group in varlist['links']:
			if group:
				yield group

def start():
	from target import targets, vectors
	from vector import vectors as vectors_info
	import methods
	
	junk = ('http://', 'https://', 'vk.com/', 'group', 'id', '/')
	if varlist['links']:
		for i, link in enumerate(varlist['links']):
			for j in junk:
				link = link.replace(j, '')
			if link.replace('-', '').isdigit():
				varlist['links'][i] = link
			else:
				myprint('Неверный формат:', varlist['links'][i], error=True)
				varlist['links'][i] = False
	
	for target_id in targets:
		vector_id, lvl = vectors[target_id]
		vector_obj = vectors_info[vector_id]
		
		myprint('{} ({})'.format(methods.names(target_id), target_id))
		if lvl == 1:
			rez = vk_request(vector_obj, 'fave.getPosts', {'count': 100})
			if rez:
				for post in rez['items']:
					print_post(post)
		else:
			for group in my_iter(vector_obj, target_id);
				print('  Анализ', group)
				posts = vk_request(vector_obj, 'wall.get', 
					{'owner_id': group, 'count': 100})
				if not posts:
					continue
				for post in posts['items']:
					like = vk_request(vector_obj, 'likes.isLiked', {
						'user_id': target_id, 
						'owner_id': -1*int(group),
						'item_id': post['id'],
						'type': 'post'})
					if like and like['liked']:
						print_post(post)
