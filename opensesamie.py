import sys
import argparse
import spacy
from collections import defaultdict
import itertools

from spacy.symbols import VERB, root
from spacy.symbols import nsubj,csubj
from spacy.symbols import dobj,iobj,obj,pobj

def getVerb(t):
	cycle = set()
	while True:
		if t.pos == VERB:
			return t
		if t.dep == root:
			return None
		if t in cycle:
			return None
		cycle.add(t)
		t = t.head

if __name__ == '__main__':
	parser = argparse.ArgumentParser('A Open Information Extraction tool for extracting relations from text')
	parser.add_argument('--inDoc',required=True,type=str,help='Plain text document to process')
	parser.add_argument('--outTSV',required=True,type=str,help='Lists of relations extracted')
	args = parser.parse_args()

	with open(args.inDoc) as inF:
		text = inF.read()

	nlp = spacy.load('en')
	doc = nlp(text)

	tokenToChunk = {}
	for chunk in doc.noun_chunks:
		tokenToChunk[chunk.root] = chunk.text

	verbs = [ t for t in doc if t.pos == VERB ]

	subjs = [ t for t in doc if t.dep in [nsubj,csubj] ]
	objs = [ t for t in doc if t.dep in [dobj,iobj,obj,pobj] ]

	subjsMapped = defaultdict(list)
	objsMapped = defaultdict(list)

	for t in subjs:
		verb = getVerb(t)
		if not verb == None:
			subjsMapped[t.head].append(t)
	for t in objs:
		verb = getVerb(t)
		if not verb == None:
			objsMapped[verb].append(t)

	with open(args.outTSV,'w') as outF:
		for v in verbs:
			for subj,obj in itertools.product(subjsMapped[v],objsMapped[v]):
				if subj in tokenToChunk:
					subjTxt = tokenToChunk[subj]
				else:
					subjTxt = subj.text
				if obj in tokenToChunk:
					objTxt = tokenToChunk[obj]
				else:
					objTxt = obj.text
				out = [ subjTxt, v.text, objTxt ]
				text = "\t".join(out)
				outF.write(text + "\n")

