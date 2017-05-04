"""Модуль для поиска комментариев пользователя в группах из списка"""

varlist = {
	'links': ' '
	}
descr = {
	'links': 'Если не указано, ищет в группах пользователя'
	}


def start():
	from __main__ import myprint, vk_request
	from target import targets, vectors
	from vector import vectors as vectors_info
	import methods
	
	junk = ('http://', 'https://', 'vk.com/', 'group', 'id', '/')
	if type(varlist['links']) is str:
		varlist['links'] = varlist['links'].strip()
	elif type(varlist['links']) is tuple:
		varlist['links'] = list(varlist['links'])
	if varlist['links']:
		if not type(varlist['links']) is list:
			varlist['links'] = [varlist['links']]
		for i, link in enumerate(varlist['links']):
			for j in junk:
				link = link.replace(j, '')
			if link.replace('-', '').isdigit():
				varlist['links'][i] = link
			else:
				myprint('Неверный формат:', varlist['links'][i], error=True)
				varlist['links'][i] = False
	
	groups = False
	if varlist['links']:
		groups =  varlist['links']
	else:
		#сообщества юзера
		groups = set()
		for target_id in targets:
			vector_id, lvl = vectors[target_id]
			vector_obj = vectors_info[vector_id]
			this_groups = vk_request(vector_obj, 'groups.get', 
				{'user_id': target_id, 'count': 1000})
			if this_groups:
				this_groups = [-1*int(group) for group in this_groups['items']]
				groups.update(set(this_groups))
	if not groups:
		myprint('  Невозможно получить список групп!', error=True)
		return
	
	for group in groups:
		myprint('\n\n{} ({})'.format(methods.names(group), group))
		posts = vk_request(methods.get_vk(), 'wall.get', 
			{'owner_id': group, 'count': 100})
		if not posts:
			continue
		
		for post in posts['items']:
			if post['from_id'] in targets:
				if len(post['text']) > 78:
					post['text'] = post['text'][:77]+'…'
				myprint('\n  {} ({})'.format(methods.names(post['from_id']), post['from_id']))
				myprint(' ', post['text'])
				myprint('  https://vk.com/wall-', group,'_', post['id'], sep='')
			
			comments = vk_request(methods.get_vk(), 'wall.getComments', {
				'owner_id': group,
				'post_id': post['id'],
				'count': 100
				})
			if not comments:
				continue
			
			for comment in comments['items']:
				if comment['from_id'] in targets:
					if len(comment['text']) > 78:
						comment['text'] = comment['text'][:77]+'…'
					myprint('\n  {} ({})'.format(methods.names(comment['from_id']), comment['from_id']))
					myprint(' ', comment['text'])
					myprint('  https://vk.com/wall', group,'_', post['id'], '?reply=', comment['id'], sep='')
