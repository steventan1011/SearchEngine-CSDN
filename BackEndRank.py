import os
import math
import re
import jieba
import json
symbol_pattern = re.compile(r'.,}{!%！？。，‘；“”’;')

# 读取停用词表
def LoadStopWord() -> list:
	with open('BackPart/stopWord.txt', 'r', encoding='utf-8') as f:
		StopWords = f.readlines()
		for i in range(len(StopWords)):
			StopWords[i] = StopWords[i][:-1]
	return StopWords

def is_symbol(word) -> bool:
	if symbol_pattern.match(word) is not None:
		return False
	else:
		return True


def VSM_search(query: str, inversal_index: dict, idf: dict, urls: dict):
	average_length = sum([urls[a]['len'] for a in urls.keys()]) / len(urls)
	cut = jieba.cut_for_search(query)
	words = [a for a in cut]
	Articles = {}
	score = []
	related_articles = []
	for i in words:
		if i in inversal_index:
			related_articles = inversal_index[i]
		else:
			break
		for j in related_articles:
			if j not in Articles:
				Articles[j] = 0

			i = i.lower()
			if i in urls[j]['tf']:
				Articles[j] += (1 + math.log(urls[j]['tf'][i])) / ((1 - 0.2) + 0.2 * urls[j]['len'] / average_length) * math.log(len(urls) / idf[i])
	for i in Articles:
		score.append((i, Articles[i]))
	result = merage(score)
	return [a[0] for a in result if a[1]!=0][:100]


def sort(List1, List2):
	a = 0
	b = 0
	result_List = []
	while a < len(List1) and b < len(List2):
		if List1[a][1] > List2[b][1]:
			result_List.append(List1[a])
			a += 1
		else:
			result_List.append(List2[b])
			b += 1
	while a < len(List1):
		result_List.append(List1[a])
		a += 1
	while b < len(List2):
		result_List.append(List2[b])
		b += 1
	return result_List


def merage(List):
	if len(List) < 2:
		return List
	else:
		mid = len(List) // 2
		List1 = merage(List[:mid])
		List2 = merage(List[mid:])
		return sort(List1, List2)

