from collections import Counter, defaultdict
import math, re
import kenlm
import operator
import itertools

model = kenlm.Model('bnc.prune.arpa')


def words(text): return re.findall(r'\w+|[,.?]', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return float(WORDS[word] / N)

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
    
def suggest(word):
    '''return top 5 words as suggestion, original_word as top1 when original_word is correct'''
    suggest_P = {}
    edits_set = edits1(word).union(set(edits2(word)))
    for candidate in known(edits_set):
        suggest_P[candidate] = P(candidate)
    if word in WORDS:
        suggest_P[word] = 1
    suggest_can = sorted(suggest_P, key=suggest_P.get, reverse=True)[:5]
    
    return suggest_can
    
def spelling_check(sentence):
    sentence = sentence.split()
    candidate = ['']
    
    known_words = known(WORDS)
    
    for word in sentence:
    	if word in known_words:
    		new_candidate = []
    		for c in candidate:
    			new_candidate.append(c + ' ' + word)
    		candidate = new_candidate
    	else:
    		new_candidate = []
    		for c in candidate:
    			for s in suggest(word):
    				new_candidate.append(c + ' ' + s)
    		candidate = new_candidate
    
    best_candidate = ''
    best_score = -100000
    
    for c in candidate:
    	if model.score(c) / len(c.split()) > best_score:
    		best_candidate = c
    		best_score = model.score(c) / len(c.split())
    
    return best_candidate, candidate




#### TASK1 ####

print("Task 1 Spelling Check")
task1_input = 'he sold everythin escept the housee'
print("Text:",task1_input,"\n")
print("Candidates:")
task1_result, task1_candidate = spelling_check(task1_input)
for i in task1_candidate[:30]:
    print(i)
print("Number of Candidate:", len(task1_candidate))
print()
print("Result:", task1_result,"\n\n\n")

#### TASK1 END ####




#### TASK2 ####

atcs = {"", "the", "a", "an"}
preps = {"", "about", "at", "by", "for", "from", "in", "of", "on", "to", "with"}

def prep_check(sentence):

	sentence = sentence.split()
	candidate = ['']
	    
	for word in sentence:
		if word in atcs or word in preps:
			new_candidate = []
			for c in candidate:
				for a in atcs:
					new_candidate.append(c + ' ' + a)
				for p in preps:
					new_candidate.append(c + ' ' + p)
			candidate = new_candidate
		else:
			new_candidate = []
			for c in candidate:
				new_candidate.append(c + ' ' + word)
			candidate = new_candidate
		
	
	best_candidate = ''
	best_score = -100000
    
	for c in candidate:
    		if model.score(c) / len(c.split()) > best_score :
    			best_candidate = c
    			best_score = model.score(c) / len(c.split()) 
    			
	print(best_candidate)
		
	return best_candidate, candidate
    
print("Task 2 Preposition and Article Check")
task2_input = 'look on an picture in the right'
print("Text:",task2_input,"\n")
task2_result, task2_candidate = prep_check(task2_input)
print("Candidates:")
for i in task2_candidate[:30]:
    print(i)
print("Number of Candidate:", len(task2_candidate))
print()
print("Result:", task2_result,"\n\n\n")

#### TASK2 END ####





#### TASK3 ####

def process_sent(sent):

	_,candidates1 = spelling_check(sent)
	
	best_candidate = ''
	best_score = -100000
	
	for c in candidates1:
		candidate2,_ = prep_check(c)
		if model.score(candidate2) / len(candidate2) > best_score:
    			best_candidate = candidate2
    			best_score = model.score(candidate2) / len(candidate2)
    			
	return best_candidate

print("Task 3 Combination")
task3_input = 'we descuss a possible meamin by that'
#task3_input = 'Never gonna geeve youd upp'
print("Text:",task3_input,"\n")
comb_result = process_sent(task3_input)
print("Result:", comb_result)
#### TASK3 END ####

task2_result, task2_candidate = prep_check('at an afternoon')

print(model.score('at an afternoon'))
print(model.score('  afternoon'))
print(model.score('afternoon'))
print(model.score('in the afternoon'))

