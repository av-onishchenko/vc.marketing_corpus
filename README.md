## Корпус
Корпус состоит и 1000 статей с сайта vc.ru, раздел маркетинг. Для обработки статей использовалась библиотека natasha

## Файлы
`*.json` - файлы с данными

`get_pages.py` - скачивание статей

`text_processing.py` - обработка статей

`paresr.py` - клиет, его надо запускать с нужными флагами для работы с корпусом

## Анализ работы
Рассмотрим грамматическую омонимию

Для разных значений слова "взрослые" правильно нааходится часть речи

![Image alt](https://github.com/av-onishchenko/vc.marketing_corpus/raw/main/pics/omon1_1.png)

![Image alt](https://github.com/av-onishchenko/vc.marketing_corpus/raw/main/pics/omon1_2.png)

Для одинакого значения слова "больной" пайплайн дает ему разные части речи

![Image alt](https://github.com/av-onishchenko/vc.marketing_corpus/raw/main/pics/omon2_1.png)

![Image alt](https://github.com/av-onishchenko/vc.marketing_corpus/raw/main/pics/omon2_2.png)

Рассмотрим лексическую омонимию

Для разных значений слова "очки" правильно нааходится часть речи

![Image alt](https://github.com/av-onishchenko/vc.marketing_corpus/raw/main/pics/omon3_1.png)

![Image alt](https://github.com/av-onishchenko/vc.marketing_corpus/raw/main/pics/omon3_2.png)

И наконец рассмотрим пример эллипса:

У предложения "В бизнесе я с 2007 года" было построенно такое дерево:

![Image alt](https://github.com/av-onishchenko/vc.marketing_corpus/raw/main/pics/ellipse1.png) 

Что выглядит странно

А вот у предложения "Работают, но недолго и плохо" было построенно такое дерево:

![Image alt](https://github.com/av-onishchenko/vc.marketing_corpus/raw/main/pics/ellipse2.png) 

Которое похоже на правду, хотя тип связи у "плохо" и "недолго" должен быть одинаковый, а модель дала и разный

## Итог
Разметка может ошибиться на омонимах, деревья зависимостей тоже имеют изьяны, особенно в предложениях без сказуемого и тем более недревесных. 

Но все эти недостатки можно покрыть скоростью разметки, ведь тысяча статей разметилась за пару минут. Такой размен скорости скорее всего важней легкой потери в качестве (особенно если хочется разметить гигантский корпус)