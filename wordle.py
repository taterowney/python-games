import random, sys

random.seed(150)

with f = open("/Users/trowney/Documents/dictionary.txt", "r"):
    dictionary = f.read()


five_letter_words= []

for word in dictionary:
    if len(word)==5:
        five_letter_words.append(word)


def generate_word():
    return five_letter_words[random.randint(0, len(five_letter_words)-1)]

def check_answer(word, target):
    if word == target:
        return ("Correct! The word was %s"% target)
    w = list(word)
    t = list(target)
    
