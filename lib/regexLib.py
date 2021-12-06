import re
from unidecode import unidecode

def reloadMeeseBlacklist():
  with open('./resources/meese_blacklist.txt', 'r') as blacklist_raw:
    global M_BLACKLIST, E_BLACKLIST, S_BLACKLIST, TRIM_CHARS
    M_BLACKLIST = []
    E_BLACKLIST = []
    S_BLACKLIST = []
    TRIM_CHARS = []
    blacklist_raw = blacklist_raw.read() + '\n'
    temp_category = "M_BLACKLIST"
    # Read blacklist, and sort into M_BLACKLIST, E_BLACKLIST, S_BLACKLIST, and TRIM_CHARS
    for line in blacklist_raw.split('\n'):
      if line.startswith('$$'):
        temp_category = line[2:].strip()
        continue
      else:
        if temp_category == "M_BLACKLIST":
          M_BLACKLIST.append(line.strip('\n'))
        elif temp_category == "E_BLACKLIST":
          E_BLACKLIST.append(line.strip('\n'))
        elif temp_category == "S_BLACKLIST":
          S_BLACKLIST.append(line.strip('\n'))
        elif temp_category == "TRIM_CHARS":
          TRIM_CHARS.append(line.strip('\n'))

MEESE_REGEX = re.compile("""me{2,}s+e""")

def reverseString(x):
  return x[::-1]

def replaceWords(words, string, replaceWith, replace=1):
  if len(words) == 0: return string
  for word in words:
    newString = string.replace(word, replaceWith, replace)
    #if newString != string:
      #print(word + ': ' + newString)
    string = newString
  return string.lower()

def containsMeese(inputStr):
  #print('ORIGINAL STRING: ' + inputStr)
  inputStr = replaceWords(TRIM_CHARS, inputStr, "", -1)
  inputStr = replaceWords(M_BLACKLIST, inputStr, "m", 32)
  inputStr = replaceWords(E_BLACKLIST, inputStr, "e", 64)
  inputStr = replaceWords(S_BLACKLIST, inputStr, "s", 32)
  #inputStr = re.sub(r'\d', '', inputStr)
  inputStr = unidecode(inputStr)
  #print('FINAL STRING: ' + inputStr)
  contains_meese = re.search(MEESE_REGEX, inputStr)
  #if contains_meese == None:
  #  contains_meese = re.search(MEESE_REGEX, reverseString(inputStr))
  if contains_meese == None:
    return False
  return True