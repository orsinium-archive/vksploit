from __main__ import vk_request, myprint
import functools
from random import choice

from target import targets, vectors
from vector import vectors as vectors_info
def get_vk(uid=False):
	if uid:
		if uid in vectors_info:
			return vectors_info[uid]
		if uid in vectors:
			vector_id, lvl = vectors[uid]
			return vectors_info[vector_id]
	return choice(list(vectors_info.values()))

@functools.lru_cache(maxsize=300)
def friends(uid, vk=False):
	if not vk:
		vk = get_vk(uid)
	rez = vk_request(vk, 'friends.get', {'user_id': uid})
	if rez:
		return set(rez['items'])
	else:
		return set()


@functools.lru_cache(maxsize=100)
def names(uid, vk=False):
	if not vk:
		try:
			vk = get_vk(uid)
		except IndexError:
			myprint('Прежде всего необходимо добавить векторы!')
			return ''
	if int(uid) > 0:
		rez = vk_request(vk, 'users.get', {'user_ids': uid})
		if rez:
			return rez[0]['first_name']+' '+rez[0]['last_name']
		else:
			return ''
	else:
		rez = vk_request(vk, 'groups.getById', {'group_ids': str(uid)[1:]})
		if rez:
			return rez[0]['name']
		else:
			return ''
		
