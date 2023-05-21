import json
from natasha import (
    Doc,
    Segmenter,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    MorphVocab
)
from tqdm import tqdm

def text_processing():
    ''' Обработка текстов '''
    # Интсрументы библиотеки
    segmenter = Segmenter()
    emb = NewsEmbedding()
    morph_vocab = MorphVocab()
    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)
    # Чтение текстов
    with open('texts.json', 'r') as fp:
        texts = json.JSONDecoder().decode(fp.read())
    # Сама обработка
    words_dict = {}
    for text_id, text in tqdm(enumerate(texts)):
        doc = Doc(". ".join(text['text'].split(".")))
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        doc.parse_syntax(syntax_parser)
        for token in doc.tokens:
            token.lemmatize(morph_vocab)
        for sent_id, sent in enumerate(doc.sents):
            for token in sent.tokens:
                # Пунктуация нам не нужна
                if token.pos == 'PUNCT':
                    continue
                if words_dict.get(token.lemma) is None:
                    words_dict[token.lemma] = []
                new_reference = {}
                # Сделаем ссылку на текст и номер предложения
                new_reference['text_id'] = text_id
                new_reference['sent_id'] = sent_id
                new_reference['sent_pos'] = sent.start, sent.stop
                new_reference['start'] = token.start
                new_reference['stop'] = token.stop
                # Соберем нужную информацию
                new_reference['original_form'] = token.text
                new_reference['pos'] = token.pos
                new_reference['rel'] = token.rel
                new_reference['feats'] = token.feats
                words_dict[token.lemma].append(new_reference)
    return words_dict

def make_corpus_file():
    ''' Функция для получения json файла с корпусом '''
    texts = text_processing()
    with open('corpus.json', 'w') as fp:
        json.dump(texts, fp)

make_corpus_file()