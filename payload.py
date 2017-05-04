from __main__ import myprint
import importlib

from inputer import pll as payloadlist
payload = False

def flist():
	for pld in payloadlist:
		print(pld)

def finfo(query=False):
	if query:
		query = query[0]
		if query not in payloadlist:
			myprint('Нагрузка не найдена!', error=True)
			return
		module = importlib.import_module('payloads.'+query)
		print('-'*80)
		print(module.__doc__)
		print('-'*80)
	else:
		print('-'*80)
		print(payload.__doc__)
		print('-'*80)
		fshow()

def fshow():
	if not payload:
		myprint('Не выбрана нагрузка!', error=True)
		return
	if 'varlist' not in payload.__dir__():
		print('Нагрузка не содержит переменных!')
		return
	
	kw = max([len(str(i)) for i in payload.varlist.keys()])
	vw = max([len(str(i)) for i in payload.varlist.values()])
	print('┌', '─'*kw, '┬', '─'*vw, '┐', sep='')
	for k, v in payload.varlist.items():
		print(('│{:'+str(kw)+'}│{:'+str(vw)+'}│{}').format(k, v, payload.descr[k]))
	print('└', '─'*kw, '┴', '─'*vw, '┘', sep='')

def fuse(query):
	global payload
	query = query[0]
	if query not in payloadlist:
		myprint('Нагрузка не найдена!', error=True)
		return
	payload = importlib.import_module('payloads.'+query)
	
	print('Нагрузка успешно подключена')
	print(payload.__doc__)
	fshow()

def fset(var, *vals):
	if not payload:
		myprint('Не выбрана нагрузка!', error=True)
		return
	if var not in payload.varlist:
		myprint('Переменная не найдена!', error=True)
		return
	
	if len(vals) == 1:
		if vals[0].isdigit():
			payload.varlist[var] = int(vals[0])
		else:
			payload.varlist[var] = vals[0]
	else:
		payload.varlist[var] = vals
	print('Переменная', var, 'успешно установлена.')

def fstart():
	if not payload:
		myprint('Не выбрана нагрузка!', error=True)
		return
	try:
		payload.start()
	except KeyboardInterrupt:
		myprint('Payload has stoped!', error=True)
	#except Exception as e:
	#	myprint(e, error=True)
