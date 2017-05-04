"""Модуль для загрузки прикреплений из постов."""

varlist = {
	'links': '',
	'dir': 'downloads'
	}
descr = {
	'links': 'ссылки на записи',
	'dir': 'директория, в которую будут сохранены скачанные файлы'
	}

def start():
	from __main__ import myprint, vk_request
	from target import targets, vectors
	from vector import vectors as vectors_info
	import methods
	
	from time import sleep
	import re
	from grab import Grab
	g = Grab()
	
	
	def download(name, link):
		myprint('Download', name+'...')
		g.setup(log_file=varlist['dir']+name, timeout=False)
		g.go(link)
		g.setup(log_file=False, timeout=14997)
	
	
	def get_photo(attach):
		size = False
		for allowed_size in photo_sizes:
			if 'photo_'+allowed_size in attach:
				size = allowed_size
				break
		if size:
			download(str(attach['owner_id'])+'_'+str(attach['id'])+'.jpg', attach['photo_'+size])
	
	
	from urllib.parse import quote
	def get_video(name, link):
		for i in (1, 2, 3):
			try:
				g.go(link)
			except Exception as e:
				myprint(e, error=True)
				sleep(i)
			else:
				break
		else:
			myprint('Не удалось получить видео!', error=True)
			return
		
		if link.startswith('https://vk.com/'):
			flink = False
			page = g.response.body.decode('utf-8')
			vk_rex = r'https\:\/\/[a-z0-9\-]+\.vk[a-z0-9\/\-\.]+\.{}'
			for i in ('720\.mp4', '480\.mp4', '360\.mp4', 'vk.flv'):
				try:
					flink = re.search(vk_rex.format(i), page).group()
				except Exception as e:
					myprint(e, error=True)
				else:
					break
			else:
				myprint('Не удалось найти ссылку для загрузки видео с vk!', error=True)
				return
			download(name, flink)
		elif link.startswith('https://coub.com/'):
			page = g.response.body.decode('utf-8')
			try:
				page = page[page.find('"html5":{"video":'):page.find(',"iphone":{"url"')]
				page = page[page.find('"url":"')+7:]
				video = page[:page.find('"')]
				page = page[page.find('"audio"'):]
				page = page[page.find('"url":"')+7:]
				audio = page[:page.find('"')]
			except Exception as e:
				myprint('Ошибка при парсинге страницы coub!', error=True)
				myprint(e, error=True)
				return
			download(name+'.mp4', video)
			download(name+'.mp3', audio)
		elif link.startswith('https://www.youtube.com/'):
			try:
				g.go('http://keepvid.com/?url='+quote(link))
				page = g.response.body.decode('utf-8')
			except Exception as e:
				myprint('Ошибка при переходе на keepvid.com!', error=True)
				myprint(e, error=True)
				return
			page = page[page.find('id="info"'):]
			for size in ('720p', '480p', '360p'):
				if size in page:
					page = page[:page.find(size)]
					page = page[page.rfind('http'):]
					link = page[:page.find('"')]
					break
			else:
				myprint('Не удалось найти ссылку для загрузки видео с youtube!', error=True)
				return
			download(name, link)
		else:
			 myprint('Невозможно скачать видео! Неподдерживаемый тип.', error=True)
			 myprint(link)
	
	
	from boilerpipe.extract import Extractor
	def get_link(name, link):
		try:
			g.go(link)
		except Exception as e:
			myprint('Ошибка при переходе по ссылке!', error=True)
			myprint(e, error=True)
			return
		try:
			g.response.detect_charset()
			rez = g.response.body.decode(g.response.charset)
		except Exception as e:
			myprint('Ошибка при декодировании страницы!', error=True)
			myprint(e, error=True)
			return
		try:
			extractor = Extractor(extractor='ArticleExtractor', html=rez)
			text = extractor.getText()
		except Exception as e:
			myprint('Ошибка при извлечении текста!', error=True)
			myprint(e, error=True)
			return
		open(varlist['dir']+name+'.html', 'w').write(rez)
		open(varlist['dir']+name+'.txt', 'w').write(text)
	
	
	photo_sizes = ('1280', '807', '604')
	
	if not varlist['links']:
		myprint('Не заданы ссылки для скачивания', error=True)
		return
	
	if varlist['dir'][-1] != '/':
		varlist['dir'] = varlist['dir'] + '/'
	if type(varlist['links']) is str:
		varlist['links'] = [varlist['links']]
	
	links = []
	for link in varlist['links']:
		if '/wall' not in link or '_' not in link:
			myprint('Неверный формат ссылки:', link, error=True)
			continue
		link = link[link.find('wall')+4:]
		links.append(link)
	
	posts = vk_request(methods.get_vk(), 'wall.getById', {'posts': ','.join(links)})
	if posts:
		#for post in posts['items']:
		for post in posts:
			if len(post['text']) > 5:
				myprint('\n'+(post['text'].replace('\n', ''))+'\n')
				open('{}description.{}_{}.txt'.format(varlist['dir'], post['owner_id'], post['id']), 'w').write(post['text'])
			if 'attachments' not in post:
				myprint('Нет прикреплений!', error=True)
				continue
			for attach in post['attachments']:
				#if attach['type'] in attach and len(attach.keys()) == 2:
				attach[attach['type']]['type'] = attach['type']
				attach = attach[attach['type']]
				
				if attach['type'] == 'photo':
					get_photo(attach)
				elif attach['type'] == 'posted_photo':
					download(str(attach['owner_id'])+'_'+str(attach['id'])+'.jpg', attach['photo_604'])
				elif attach['type'] == 'video':
					video = vk_request(methods.get_vk(), 'video.get', {
						'videos': str(attach['owner_id'])+'_'+str(attach['id'])})
					if video and 'player' in video['items'][0]:
						get_video(attach['title'], video['items'][0]['player'])
					else:
						myprint('Видео', attach['title'], 'недоступно для скачивания...', error=True)
				elif attach['type'] == 'audio':
					download(attach['artist']+' - '+attach['title']+'.mp3', attach['url'])
				elif attach['type'] == 'doc':
					download(attach['title']+'.'+attach['ext'], attach['url'])
				elif attach['type'] == 'link':
					myprint('Сохранение', attach['title']+'...')
					get_link(attach['title'], attach['url'])
				elif attach['type'] == 'note':
					open(varlist['dir']+attach['title']+'.txt', 'w').write(attach['text'])
				elif attach['type'] == 'page':
					get_link(attach['view_url'], attach['url'])
				elif attach['type'] == 'album':
					photos = vk_request(methods.get_vk(), 'photos.get', {'album_id': attach['id']})
					if photos:
						for photo in photos['items']:
							get_photo(photo)
				else:
					myprint('Неподдерживаемый тип:', attach['type'], error=True)
