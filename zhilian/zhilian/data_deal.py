# -*- coding: utf-8 -*-
import jieba
import pandas as pd
import numpy
from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator

def Frequency(detail):
    segment = jieba.lcut(detail)
    word_df = pd.DataFrame({'segment': segment})
    stopwords = pd.read_csv("stopwords.txt", index_col=False, quoting=3, sep=" ", names=['stopword'],
                            encoding='utf-8')
    word_df = word_df[~word_df.segment.isin(stopwords.stopword)]
    words_stat = word_df.groupby(by=['segment'])['segment'].agg({"count": numpy.size})
    words_stat = words_stat.reset_index().sort_values(by=["count"], ascending=False)
    print(words_stat)
    # word_frequence = {x[0]: x[1] for x in words_stat.head(100).values}
    word_frequence = {}
    for segment,row in words_stat.iterrows():
        segment,count = row
        word_frequence.setdefault(segment,count)
    print(word_frequence)
    word_cloud(word_frequence)

def word_cloud(words):
    bg_pic = imread('Python.png')
    image_colors = ImageColorGenerator(bg_pic)
    wc = WordCloud(
        font_path='msyh.ttf',
        background_color='white',
        max_words=100,
        mask=bg_pic,
        max_font_size=50,
        color_func=image_colors,
    )
    wc.generate_from_frequencies(words)
    plt.figure()
    wc.to_file('Job.png')
    plt.imshow(wc)
    plt.axis('off')
    plt.show()