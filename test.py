import re    
text = "Hello World       How     Are Yout"

# Split the string into a list of words
words = re.split(r'\s{2,}', text)
print(words)