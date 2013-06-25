import sys, re

fp = open("mpaa-ratings-reasons.list")
data = fp.read()
fp.close()
lines = data.split('\n')
db = dict()

remv = re.compile('^MV: ')
rere = re.compile('^RE: ')
remvf = re.compile('^MV: (.*) (\(([0-9]{4})(/[IV]+)?\))( (.*) *)?$')
reref = re.compile('^RE: Rated ([^ ]+) (for|on) (.+)$')
reref2 = re.compile('^RE: (.+)$')
reref3 = re.compile('^RE: Rating surrendered; (.+)$')

state = 0
title = None
date = None
other = None
rating = None
reason = None
results = list()

for l in lines:
  if len(l) == 0:
    state = 0
    title = None
    continue

  mvfound = remv.search(l)
  refound = rere.search(l)

  str = ">> "+l
  if mvfound: str += "; mvfound"
  if refound: str += "; refound"
  str += '; state: %d' % (state,)
  #print(str)

  if state == 0 and mvfound:
    hit = remvf.search(l)
    if hit:
      if hit.group(3) is not None:
	title = hit.group(1)
	date = hit.group(3)
	if hit.group(4) is not None:
	  other = hit.group(5)
	else:
	  other = ''
	rating = None
	reason = None
	state += 1
      else:
	print('error 1 on: '+l)
	title = None
    else:
      print('error 2 on: '+l)
      title = None
  elif state == 1 and refound:
    hit = reref.search(l)
    if hit:
      if hit.group(3) is not None:
	rating = hit.group(1)
	reason = hit.group(3)
	state += 1
      else:
	print('error 3 on: '+l)
	state = 0
	title = None
    else:
      hit = reref3.search(l)
      if hit:
	rating = "Unrated"
	reason = hit.group(1)
	state += 1
      else:
	print('error 4(%d) on: %s' % (state,l))
	state = 0
	title = None
  elif state == 2 and refound:
    hit = reref2.search(l)
    if hit:
      if len(hit.groups()) == 1:
	reason += ' '+hit.group(1)
      else:
	print('error 5 on: '+l)
	state = 0
	title = None
    else:
      print('error 6 on: '+l)
      state = 0
      title = None
  elif refound or mvfound:
    print('continuity error, state=%d; %s' % (state,l))
    state = 0
    title = None
  elif ( state == 1 or state == 2 ):
      #print('error: no detect on state = 1 or 2, reset')
    state = 0
    title = None
  else:
    #print('hit the bottom else, reset')
    #print("..")
    state = 0

  if state == 0 and title is not None:
    if date is None: date = '?'
    if other is None: other = ''
    if rating is None: rating = '?'
    if reason is None: reason = '?'
    results.append("\t".join([title,date,other,rating,reason]))
    title = None
    date = None
    other = None

print('made it through the list')
fp = open('Rresults.tab','w')
fp.write('\n'.join(results))
fp.close()


