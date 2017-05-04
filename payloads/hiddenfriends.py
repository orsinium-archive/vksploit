"""Ищет всех друзей пользователя, включая скрытых"""

varlist = {
	'depth': 2,
	'min_users': 20,
	'max_users': 60
	}
descr = {
	'depth': 'Глубина обхода списка друзей',
	'min_users': 'Мин. число людей, рассматриваемых в каждом списке друзей',
	'max_users': 'Макс. число людей, рассматриваемых в каждом списке друзей'
	}

def start():
	from __main__ import myprint, vk_request
	from target import targets, vectors
	from vector import vectors as vectors_info
	import methods
	
	def get_friends(uid, target, lvl=1):
		global finded_friends
		lfriends = methods.friends(uid)
		if not lfriends:
			return False
		
		founded_in_this_list = False
		#если нашли нового друга
		if target in lfriends and uid not in get_friends.founded:
			founded_in_this_list = True
			get_friends.founded.append(uid)
			myprint('{} ({})'.format(methods.names(uid), uid))
		
		#если в данном списке найдена цель, можно нырнуть на два уровня глубже
		if lvl <= varlist['depth'] \
		or (founded_in_this_list and lvl <= varlist['depth']+2):
			#если цель была найдена, рассматриваем по максимуму людей из этого списка
			limit = varlist['max_users'] if founded_in_this_list else varlist['min_users']
			for i, friend in enumerate(lfriends):
				#снижает число зацикливаний
				if friend not in get_friends.founded:
					if i >= limit:
						break
					rez = get_friends(friend, target, lvl+1)
					#если было попадание в подсписке, рассматриваем по максимуму людей из этого списка
					if rez:
						limit = varlist['max_users']
		return founded_in_this_list
	
	for target_id in targets:
		vector_id, lvl = vectors[target_id]
		lfriends = methods.friends(target_id)
		get_friends.founded = []
		if lfriends:
			get_friends.founded = list(lfriends)
			print('Visible:')
			for uid in lfriends:
				myprint('{} ({})'.format(methods.names(uid), uid))
			print('\nHidden:')
		if lfriends and len(lfriends) > 5:
			for uid in lfriends:
				get_friends(uid, target_id)
		else:
			get_friends(vector_id, target_id)
