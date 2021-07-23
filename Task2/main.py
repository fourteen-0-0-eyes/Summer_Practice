from typing import List


def start_hangman(words: List[str]):
    if len(words) in range(10, 16):
        from random import randint
        word = words[randint(1, len(words) - 1)].lower()
        hidden_word = ['_' for _ in word]
        mistakes = 0
        print(*hidden_word)
        while mistakes < 10 and '_' in hidden_word:
            input_letter = input().strip().lower()
            if len(input_letter) == 1 and input_letter.isalpha():
                if input_letter in word:
                    for i in range(len(word)):
                        if word[i].lower() == input_letter:
                            hidden_word[i] = input_letter
                if input_letter not in word:
                    mistakes += 1
                    if mistakes < 10:
                        print(f'There is no such letter. Attempts left: {10 - mistakes}')
            else:
                print('Incorrect input.')
            if mistakes < 10:
                print(*hidden_word)
        if '_' in hidden_word:
            print('You lose.')
        else:
            print('Congratulations! You win :)')
    else:
        print('Incorrect words count')


if __name__ == '__main__':
    with open('words.txt', 'r', encoding='utf-8') as file_r:
        data = file_r.read().split('\n')
    start_hangman(data)
