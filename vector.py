from vk import Session, API
from __main__ import myprint, vk_request
import target

#uid -> obj
from pickle import load
try:
	utokens = load(open('vectors', 'rb'))
except:
	utokens = []
vectors = dict()
if utokens:
	for token, uid in utokens:
		vectors[uid] = API(Session(access_token=token))

import methods

def flist():
	print('Доступные:')
	i = 1
	for uid, obj in vectors.items():
		print('{:>2}. {} ({})'.format(i, methods.names(uid, obj), uid))
		i += 1
	print('Установленные:')
	i = 1
	for uid, info in target.vectors.items():
		print('{:>2}. {} -> {} ({} ур.)'.format(i, info[0], uid, info[1]))
		i += 1

from config import APP_KEY
def fadd(query):
	global vectors
	global utokens
	if not query:
		print('https://oauth.vk.com/authorize?client_id=' + APP_KEY + \
			'&scope=4667422&display=page&v=5.44&response_type=token')
	else:
		for token in query:
			token = token[token.find('access_token=')+13:]
			uid = int(token[token.rfind('=')+1:])
			token = token[:token.find('&')]
			if uid in vectors:
				myprint('Токен уже есть в списке!', error=True)
			else:
				try:
					vk = API(access_token=token)
				except Exception as e:
					myprint(e, error=True)
				else:
					utokens.append((token, uid))
					name = methods.names(uid, vk)
					vectors[uid] = vk
					myprint('Вектор добавлен: {} ({})'.format(name, uid))

def fdelete(query):
	global vectors
	for uid in query:
		if uid in vectors:
			vectors.pop(uid)
			print(uid, 'успешно удален из списка векторов.')
		else:
			myprint('Вектор не найден!', error=True)

def fget(queries):
	for query in queries:
		query = int(query)
		#Если цель есть в списке векторов
		if query in vectors:
			target.vectors[query] = (query, 1)
			print('Для {0} ({1}) получен вектор I уровня: {0} ({1}).'.format(
				methods.names(query),
				query))
			continue
		
		#выбрать первый вектор из списка для выполнения запросов к api
		uid = utokens[0][1]
		vk = vectors[uid]
		
		#есть ли в списке друзей выбранного вектора цель?
		friends = methods.friends(uid, vk)
		if not friends:
			myprint('Не удалось получить список друзей для', uid, error=True)
		elif query in friends:
			target.vectors[query] = (uid, 2)
			print('Для {} ({}) получен вектор II уровня: {} ({}).'.format(
				methods.names(query), 
				query, 
				methods.names(uid),
				uid
				))
			continue
		
		#есть ли в списке друзей цели какой-нибудь вектор?
		friends = methods.friends(query, vk)
		if not friends:
			myprint('Не удалось получить список друзей для', query, error=True)
		else:
			rez = friends & set(vectors)
			if len(rez):
				rez = rez.pop()
				target.vectors[query] = (rez, 2)
				print('Для {} ({}) получен вектор II уровня: {} ({}).'.format(
					methods.names(query), 
					query, 
					methods.names(rez),
					rez
					))
				continue
		
		#Есть ли общие друзья у какого-нибудь вектора и цели?
		b = False
		if friends:
			for vid, obj in vectors.items():
				friends2 = methods.friends(vid, obj)
				if friends2:
					rez = friends & friends2
					if len(rez):
						target.vectors[query] = (vid, 3)
						print('Для {} ({}) получен вектор III уровня: {} ({}).'.format(
							methods.names(query), 
							query, 
							methods.names(vid),
							vid
							))
						b = True
						break
		if b:
			continue
		
		#Выбрать случайный вектор
		target.vectors[query] = (uid, 4)
		print('Для {} получен вектор IV уровня: {}.'.format(query, uid))
