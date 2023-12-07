from hazm import *
import re

def regex_replace_(text, patterns: list, start: list = None, end: list = None):
  for i, p in enumerate(patterns):
    matches = re.finditer(p, text)
    for m in matches:
      matched = m.group().strip()
      # print('Matched:', matched)
      if end[i]:
        pattern = matched + ' ' + end[i]
      else:
        pattern = matched
      # print('Pattern:', pattern)
      if start[i]:
        text = re.sub(pattern, start[i] + ' ' + matched, text)
        # print(start[i] + ' ' + matched)
      else:
        text = re.sub(pattern, matched, text)
      # print('New Text', text)
  return text

# text = "با وقوع سیلاب، خسارت های بسیار رسید کشاورزان را."
text = "فرمان داد مرد را که بر دار آویخته شود."
# text = "بدان که خدای تعالی، قوّتی به پیغمبران، صلوات اللّه علیهم اجمعین، داده است و قوّة دیگر بپادشاهان،"
# text = 'از به با در برای و یا که نه چون چه سپس پس'
# patterns=['(\S+ )(?=را که)', '(?<!که)( \S+ )(?=را)|(^\S+ )(?=را)']
patterns=['(\S+ را )(?=که)', '(?<!که)( \S+ )(?=را)|(^\S+ )(?=را)']
start = ['که', 'به']
# end = ['را که', 'را']
end = ['که', 'را']
text = regex_replace_(text, patterns, start, end)
# # print('1', text)
# matches = re.finditer('(\S+ را )(?=که)', text)
# for m in matches:
#   finding = m.group()
#   pattern = finding.strip() + ' که'
#   text = re.sub(pattern, 'که ' + finding.strip(), text)
# # print('2', text)
# matches = re.finditer('(?<!که)( \S+ )(?=را)|(^\S+ )(?=را)', text)
# for m in matches:
#   finding = m.group()
#   pattern = finding.strip() + ' را'
#   text = re.sub(pattern, 'به ' + finding.strip(), text)
# # print('3', text)
# print(text)

normalizer = Normalizer()
lemmatizer = Lemmatizer()
words = [w for w in word_tokenize(normalizer.normalize(text))]
pos_tagger = POSTagger(model='/content/drive/MyDrive/CurrentData/pos_tagger.model')
pos = pos_tagger.tag(words)
# print(pos)
parts = []
# part_number = -1
curr_word = []
curr_pos = []
for i in range(len(pos)):
  if pos[i][1] == 'PUNCT':
    if 'VERB' in curr_pos and curr_pos[-1] != 'VERB' and curr_pos.index('VERB') != len(curr_pos)-1:
      last_verb_index = max(i for i, v in enumerate(curr_pos) if v == 'VERB')
      # verb = curr_word[last_verb_index]
      compound_verb = curr_pos[last_verb_index-1] == 'VERB'
      parts.append(curr_word[:])
      del parts[-1][last_verb_index]
      del curr_pos[last_verb_index]
      if compound_verb:
        del parts[-1][last_verb_index-1]
        del curr_pos[last_verb_index-1]
        parts[-1].append(curr_word[last_verb_index-1])
        curr_pos.append('VERB')

      parts[-1].append(curr_word[last_verb_index])
      # parts[-1].remove(verb)
      # curr_pos.remove('VERB')
      # parts[-1].append(verb)
      curr_pos.append('VERB')
    else:
      parts.append(curr_word[:])
    # if 'SCONJ' in curr_pos and curr_pos[curr_pos.index('SCONJ')-1] == 'ADP':
    #   sconj_index = curr_pos.index('SCONJ')
    #   sconj = curr_word[sconj_index]
    #   curr_pos[sconj_index] = 'ADP'
    curr_word.clear()
    curr_pos.clear()
  else:
    curr_word.append(pos[i][0])
    curr_pos.append(pos[i][1])
for p in parts:
  print(' '.join(p))

# def regex_replace_(text, patterns: list, start: list = None, end: list = None):
#   for i, p in enumerate(patterns):
#     matches = re.finditer(p, text)
#     for m in matches:
#       matched = m.group().strip()
#       # print('Matched:', matched)
#       if end:
#         pattern = matched + end[i]
#       else:
#         pattern = matched
#       # print('Pattern:', pattern)
#       if start:
#         text = re.sub(pattern, start[i] + matched, text)
#         # print(start[i] + ' ' + matched)
#       else:
#         text = re.sub(pattern, matched, text)
#       # print('New Text', text)
#   return text

# # text = "با وقوع سیلاب، خسارت های بسیار رسید کشاورزان را."
# text = "فرمان داد مرد را که بر دار آویخته شود."
# patterns=['(\S+ را )(?=که)', '(?<!که)( \S+ )(?=را)|(^\S+ )(?=را)']
# start = ['که ', 'به ']
# end = [' که', ' را']
# text = regex_replace_(text, patterns, start, end)
# # # print('1', text)
# # matches = re.finditer('(\S+ را )(?=که)', text)
# # for m in matches:
# #   finding = m.group()
# #   pattern = finding.strip() + ' که'
# #   text = re.sub(pattern, 'که ' + finding.strip(), text)
# # # print('2', text)
# # matches = re.finditer('(?<!که)( \S+ )(?=را)|(^\S+ )(?=را)', text)
# # for m in matches:
# #   finding = m.group()
# #   pattern = finding.strip() + ' را'
# #   text = re.sub(pattern, 'به ' + finding.strip(), text)
# # # print('3', text)
# print(text)

# normalizer = Normalizer()
# lemmatizer = Lemmatizer()
# words = [w for w in word_tokenize(normalizer.normalize(text))]
# pos_tagger = POSTagger(model='/content/drive/MyDrive/CurrentData/pos_tagger.model')
# pos = pos_tagger.tag(words)
# # print(pos)
# parts = []
# # part_number = -1
# curr_word = []
# curr_pos = []
# for i in range(len(pos)):
#   if pos[i][1] == 'PUNCT':
#     if 'VERB' in curr_pos and curr_pos[-1] != 'VERB' and curr_pos.index('VERB') != len(curr_pos)-1:
#       last_verb_index = max(i for i, v in enumerate(curr_pos) if v == 'VERB')
#       # verb = curr_word[last_verb_index]
#       compound_verb = curr_pos[last_verb_index-1] == 'VERB'
#       parts.append(curr_word[:])
#       del parts[-1][last_verb_index]
#       del curr_pos[last_verb_index]
#       if compound_verb:
#         del parts[-1][last_verb_index-1]
#         del curr_pos[last_verb_index-1]
#         parts[-1].append(curr_word[last_verb_index-1])
#         curr_pos.append('VERB')

#       parts[-1].append(curr_word[last_verb_index])
#       # parts[-1].remove(verb)
#       # curr_pos.remove('VERB')
#       # parts[-1].append(verb)
#       curr_pos.append('VERB')
#     else:
#       parts.append(curr_word[:])
#     # if 'SCONJ' in curr_pos and curr_pos[curr_pos.index('SCONJ')-1] == 'ADP':
#     #   sconj_index = curr_pos.index('SCONJ')
#     #   sconj = curr_word[sconj_index]
#     #   curr_pos[sconj_index] = 'ADP'
#     curr_word.clear()
#     curr_pos.clear()
#   else:
#     curr_word.append(pos[i][0])
#     curr_pos.append(pos[i][1])
# for p in parts:
#   print(' '.join(p))
