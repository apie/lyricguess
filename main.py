#!/usr/bin/env python3
# Guess the missing word in a song lyric!
# By Apie
# 2024-04-16
import re
from pathlib import Path
from random import choice, shuffle, randint
from sys import argv

print('Can you guess the missing words in this song?')
print('-' * 80)

correctly_answered = 0
wrongly_answered = 0

lyric_files = list(Path('lyrics').glob('**/*.txt'))
# print(f"{len(lyric_files)=}")
if len(argv) > 1:
    lyric_files = list(filter(lambda fn: ' '.join(argv[1:]) in ' '.join(fn.parts[1:]).lower(), lyric_files))
lyric_filename = choice(lyric_files)
# print(lyric_filename.name)
with open(lyric_filename, 'r') as f:
    lyric = list(map(str.strip, f.readlines()))
paragraphs = []
paragraph = []
for line in lyric:
    if line:
        paragraph.append(line)
    else:
        paragraphs.append(paragraph.copy())
        paragraph.clear()

print()
for paragraph in paragraphs:
    for i, line in enumerate(paragraph, 1):
        last_word = None
        if i == len(paragraph):  # last line
            # get last word from last sentence of paragraph
            words = line.split()
            last_word = words[-1]
            # strips non word characters like dots
            last_word = re.findall(r'\w+', last_word)[0]

            # Replace letters with fixed length underscores.
            words[-1] = words[-1].replace(last_word, '____')
            line = ' '.join(words)
        print(line)
        if last_word:
            print()
            new_guess_word = last_word
            i = 0
            while new_guess_word == last_word and i < 10:
                random_paragraph = randint(0, len(paragraphs) - 1)
                new_guess_word = re.findall(
                    r'\w+',
                    paragraphs[random_paragraph][-1].split()[-1],
                )[0]
                i += 1
            guess_words = [last_word, new_guess_word]
            shuffle(guess_words)
            for i, guess_word in enumerate(guess_words, 1):
               print(f"{i}. {guess_word}")
            choice = 0
            while choice < 1 or choice > len(guess_words):
                try:
                    choice = int(input('Guess! >>>') or 0)
                except ValueError:
                    pass
            guess = guess_words[choice - 1]
            print('You guessed:', guess)
            if guess == last_word:
                print('CORRECT!')
                correctly_answered += 1
            else:
                print("I'm sorry, that is not correct. The correct word was:", last_word)
                wrongly_answered += 1
    print()

score = correctly_answered / (correctly_answered + wrongly_answered)
print(f"That's the end of the song! Your score: {100 * score:.0f}%")
if score == 1:
    print('Superfan!')
elif score > .8:
    print('Awesome job!')
elif score > .6:
    print('Getting there!')
else:
    print('Keep practicing!')
