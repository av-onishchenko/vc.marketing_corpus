from corpus import get_info
from colorama import Style, Fore
import argparse

def __main__():
    parser = argparse.ArgumentParser(description='Build index.')
    parser.add_argument('--num_of_samples', action='store', default=2)
    parser.add_argument('--exact_form', action='store_true')
    args = parser.parse_args()
    while True:
        input_word = input(Fore.BLUE + 'Введите слово:' + Style.RESET_ALL)
        if input_word == 'break':
            break
        get_info(input_word, args.exact_form, int(args.num_of_samples))

if __name__ == '__main__':
    __main__()