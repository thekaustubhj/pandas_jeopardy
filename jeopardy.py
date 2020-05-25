import pandas as pd
import numpy as np
import re

pd.set_option('display.max_colwidth', -1)

jeopardy = pd.read_csv('jeopardy.csv', delimiter = ',')
print(jeopardy.info())
#print(jeopardy.describe())

jeopardy.rename(columns = {
'Show Number' : 'show_number',
' Air Date': 'air_date',
' Round' : 'round',
' Category' : 'category',
' Value' : 'value',
' Question' : 'question',
' Answer' : 'answer'}, inplace = True)

print(jeopardy.info())
print(jeopardy.head())

for i in range(7) :
  column = jeopardy.iloc[:,i]
  print(column.head())
  print(column.value_counts())

def num_converter(string) :
  if string == 'None' :
    return 0
  string = string.replace('$', '')
  string = string.replace(',', '')
  num = float(string)
  return num

jeopardy['value_float'] = jeopardy['value'].apply(lambda x : num_converter(str(x)))

print(jeopardy['value_float'].head())
print(jeopardy['value_float'].value_counts())

word_list = ['king','queen']

def word_finder(wordlist, question) :
  for word in wordlist :
    match_string = r'\b' + word + r'\b'
    match_result = re.search(match_string, question, re.IGNORECASE)
    if match_result == None :
      continue
    else :
      return 1
  return 0

jeopardy['of_interest'] = jeopardy['question'].apply(lambda x : word_finder(word_list, str(x)))
filtered = jeopardy[jeopardy['of_interest'] == 1]

print(filtered['question'].head())
print(len(filtered))

difficulty_level = filtered['value_float'].mean()
print('Difficulty Level of questions with the words')
print(word_list)
print('is ', difficulty_level)


unique_counter = filtered.groupby('answer')['question'].count().reset_index().sort_values('question', ascending = False)

print(unique_counter)

#Is there a connection between the round and the category? Are you more likely to find certain categories, like "Literature" in Single Jeopardy or Double Jeopardy?

category_dist = jeopardy.groupby(['round', 'category'])['question'].count().reset_index()
print(category_dist)

pivoted = category_dist.pivot(columns = 'round',
index = 'category', values = 'question').reset_index()
pivoted.fillna(0, inplace = True)
print(pivoted)

double_jeopardy = pivoted[pivoted['Double Jeopardy!'] > 0].sort_values('Double Jeopardy!', ascending = False)
print(double_jeopardy)

final_jeopardy = pivoted[pivoted['Final Jeopardy!'] > 0].sort_values('Final Jeopardy!', ascending = False)
print(final_jeopardy)
