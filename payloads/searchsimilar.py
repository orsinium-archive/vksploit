"""Нагрузка для поиска пользователей, похожих на заданные цели."""

def start():
	from __main__ import myprint, vk_request
	from target import targets, vectors
	from vector import vectors as vectors_info
	import methods
	
	query_fields = 'verified,sex,city,country,home_town,has_photo,education,bdate,followers_count,interests,music,movies,books,games'
	most = ['verified', 'sex', 'city', 'country', 'home_town', 'has_photo', 'education', 'first_name']
	avg = ['bdate', 'followers_count']
	cntr = ['interests', 'music', 'movies', 'books', 'games']
	
	uids = ','.join([str(target_id) for target_id in targets])
	users = vk_request(methods.get_vk(), 'users.get', {
		'user_ids': uids,
		'fields': query_fields})
	if not users:
		return
	
	#раскидываем данные о пользователях по полям
	from itertools import chain
	stat = dict.fromkeys(query_fields.split(','))
	stat.update(dict.fromkeys([i+'_count' for i in cntr]))
	stat.update({'first_name': None})
	for user in users:
		for field in chain(most, avg, cntr):
			if field in user:
				data = user[field]
				if data:
					if field == 'bdate':
						data = data[-4:]
						if '.' in data:
							continue
					elif field in ('city', 'country'):
						data = data['id']
					elif field == 'hometown':
						data = data['title']
					
					if type(data) is str and data.isdigit():
						data = int(data)
					if field in user and data:
						if stat[field] is None:
							stat[field] = [data]
						else:
							stat[field].append(data)
	
	#рассчитываем поля
	from pprint import pprint
	pprint(stat)
	count_users = len(users)
	from collections import Counter
	for field in most:
		if stat[field]:
			data = Counter(stat[field])
			data = data.most_common(1)
			if len(data):
				data = data[0]
				if data[1] > count_users/2:
					stat[field] = data[0]
				else:
					stat[field] = None
			else:
				stat[field] = None
	for field in avg:
		if stat[field]:
			stat[field] = round(sum(stat[field])/len(stat[field]))
	for field in cntr:
		if stat[field]:
			#stat[field+'_count'] = round(sum(stat[field])/len(stat[field]))
			data = Counter(stat[field])
			data = data.most_common(1)
			if len(data):
				data = data[0]
				if data[1] > max(count_users/4, 2):
					stat[field] = data[0]
				else:
					stat[field] = None
			else:
				stat[field] = None
	
	#вывод собранной статистики
	for field in chain(most, avg, cntr):
		if stat[field] is not None:
			data = stat[field]
			if field == 'sex':
				data = ('женский', 'мужской')[data - 1]
			print('{:15}: {}'.format(field, data))
	
	#формируем запрос
	fields = ['city', 'country', ('hometown', 'home_town'), 
		('university', 'education'), 'sex', ('birth_year', 'bdate'),
		'has_photo', 'interests', ('q', 'first_name')]
	query = dict()
	for field in fields:
		if type(field) is tuple:
			field1, field2 = field
		else:
			field1, field2 = field, field
		if stat[field2] is not None:
			query[field1] = stat[field2]
	
	query['fields'] = query_fields
	query['count'] = 5 #200
	if stat['followers_count'] and stat['followers_count'] > 200:
		query['sort'] = 0
	else:
		query['sort'] = 1
	
	users = vk_request(methods.get_vk(), 'users.search', query)
	print()
	for user in users['items']:
		print('{} {}\n    https://vk.com/id{}'.format(
			user['first_name'],
			user['last_name'],
			user['id']
			))
