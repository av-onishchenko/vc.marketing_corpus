import json
from natasha import (
    Doc,
    Segmenter,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    MorphVocab
)
import numpy as np
from colorama import Style, Fore

div = '-----------------------------------------------------------------------------------------------------------'

def make_sent_to_input(doc, reference):
    ''' Формирование строки и вывод ее в консоль '''
    sent_start, sent_end = reference['sent_pos']
    first_part = doc.text[sent_start:reference['start']] 
    middle = doc.text[reference['start'] : reference['stop']]
    last_part = doc.text[reference['stop']:sent_end]
    print(Fore.BLUE + 'Часть речи: ' + Style.RESET_ALL ,reference['pos'])
    print(Fore.BLUE + 'Тип связи: ' + Style.RESET_ALL, reference['rel'])
    print(Fore.BLUE +'Морфологические признаки: ' + Style.RESET_ALL, reference['feats'])
    print(Fore.BLUE + 'Предложениe: ' + Style.RESET_ALL + first_part + Fore.RED + middle + Style.RESET_ALL + last_part)
    print(Fore.BLUE + 'Синтаксический разбор: '+ Style.RESET_ALL)
    doc.sents[reference['sent_id']].syntax.print()

def get_first_form(word):
    ''' Находим начальную форму '''
    segmenter = Segmenter()
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    morph_vocab = MorphVocab()
    # Находим начальную форму
    doc = Doc(word)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tokens[0].lemmatize(morph_vocab)
    doc.tokens[0].lemma
    return doc.tokens[0].lemma

def get_exact_pos(word, first_form, df):
    ''' Находим точные вхождения слова '''
    # Находим среди тех вхождений, у которых начальная форма такая же
    idxs = []
    for idx in range(len(df[first_form])):
        if df[first_form][idx]['original_form'] == word:
            idxs.append(idx)
    return idxs

def get_info(word, find_exact=False, num_of_samples=5):
    ''' Получаем информацию о слове '''
    with open('texts.json', 'r') as fp:
        texts = json.JSONDecoder().decode(fp.read())
    with open('corpus.json', 'r') as fp:
        corpus = json.JSONDecoder().decode(fp.read())
    first_form = get_first_form(word)
    segmenter = Segmenter()
    emb = NewsEmbedding()
    syntax_parser = NewsSyntaxParser(emb)
    # Если нет упоминаний, выводим ноль
    if corpus.get(first_form) is None:
        print(Fore.BLUE + 'Общее число упомнианий: ' + Style.RESET_ALL, 0)
        print(div)
        return
    pos = np.arange(len(corpus[first_form]))
    # Если нужны точные сопадения, то необходимо их найти
    if find_exact:
        pos = get_exact_pos(word, first_form, corpus)
    real_num_of_samples = len(pos)
    print(Fore.BLUE + 'Общее число упомнианий: ' + Style.RESET_ALL, real_num_of_samples)
    # Выбираем случайное число семплов
    np.random.shuffle(pos)
    num = min(real_num_of_samples, num_of_samples)
    pos = pos[:num]
    # Выводим каждый из семплов
    for i in range(len(pos)):
        reference = corpus[first_form][pos[i]]
        doc = Doc(texts[reference['text_id']]['text'])
        doc.segment(segmenter)
        doc.parse_syntax(syntax_parser)
        make_sent_to_input(doc, reference)
        print(Fore.BLUE + 'Ссылка на статью: ' + Style.RESET_ALL + texts[reference['text_id']]['url'])
        print(div)
