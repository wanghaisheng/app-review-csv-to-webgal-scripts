import os
import csv
from random import random
from turtle import position
from unittest import TestSuite
from sentence_splitter import SentenceSplitter, split_text_into_sentences
import textwrap
from plane import *
import budoux
import re
from s1 import SrcType
import time
import random


from PIL import Image
from autocrop import Cropper


from functools import partial

buffer=2**16
cropper = Cropper()

# Get a Numpy array of the cropped image

splitter = SentenceSplitter(language='en')
resentencesp = re.compile('([,﹒﹔﹖﹗．；。！？]["’”」』]{0,2}|：(?=["‘“「『]{1,2}|$))')

def list_videos(folder):
    # list files in img directory
    files=[]
    for r, d, f in os.walk(folder):
        with os.scandir(r) as i:
            print('detecting----------',r)
            for entry in i:
                if entry.is_file():
                    filename = os.path.splitext(entry.name)[0]
                    ext = os.path.splitext(entry.name)[1]
                    # print(filename,'==',ext) 

                    start_index=1
                    if ext in ('.png', '.jpg'):
                        files.append(filename+ext)
    return files
figures=list_videos(r'D:\Download\audio-visual\saas\capcut\reviews-to-video\WebGAL-release\WebGAL\game\figure')
bgfiles=list_videos(r'D:\Download\audio-visual\saas\capcut\reviews-to-video\WebGAL-release\WebGAL\game\background')
print('loading figure',len(figures))
print('loading bg',len(bgfiles))
def splitsentence(sentence):
    s = sentence
    slist = []
    for i in resentencesp.split(s):
        if resentencesp.match(i) and slist:
            slist[-1] += i
        elif i:
            slist.append(i)
    return slist
def spliteKeyWord_en(str):
    # sent_text = nltk.sent_tokenize(str)  # this gives us a list of sentences
    # # now loop over each sentence and tokenize it separately
    # words = []
    # for sentence in sent_text:
    #     tokenized_text = nltk.word_tokenize(sentence)
    #     # tagged = nltk.pos_tag(tokenized_text)
    #     words.extend(tokenized_text)
    words = segment(punc.remove(str))    

    return words



def TextCorrectorbeforeTTS(txt):
    p = Plane()
    txt=txt.replace('&#x200B;','')
    punc.remove(txt)
    # update() will init Plane.text and Plane.values
    p.update(txt).replace(URL, '').text
    # update() will init Plane.text and Plane.values
    p.update(txt).replace(HTML, '').text
    # print(result)
    # ASCII = build_new_regex('ascii', r'[a-zA-Z0-9]+', ' ')
    # WORDS = ASCII + CHINESE_WORDS
    CN_EN_NUM = sum([CHINESE, ENGLISH, NUMBER])

    txt =' '.join([t.value for t in list(extract(txt, CN_EN_NUM))])
    return txt


def spliteKeyWord_zh(str):
    words = segment(punc.remove(str))    

    # words = jieba.lcut(str)
    return words

def long_cjk_text2paragraph_budouX(text, text_len, lang,count):
    parser = budoux.load_default_japanese_parser()
    if lang in ['en','zh', 'jp', 'kr']:
        text_len = text_len/2
        # 由于text_len实际上是word个数，但中文是没有空格的，英文词的个数相当于2倍
        results = parser.parse(text)
        words = spliteKeyWord_zh(text)
        # print('budoux：', results)
    else:
        # 都是用句号分割的 但我要逗号也分开
        # results = tokenize.sent_tokenize(text)
        # print('nltk: ',results)
        rawresults = splitsentence(text)
        words = spliteKeyWord_en(text)

        results = []
        # print('raw results;', rawresults)
        for r in rawresults:
            if len(r.split(' ')) > text_len:
                # print('this line is too loog', r)
                wrapper = textwrap.TextWrapper(
                    width=text_len, break_long_words=False, replace_whitespace=False)
                text = wrapper.wrap(text=r)
                for t in text:
                    print('add line break', t)
                    results.append(t+' ')
            else:
                results.append(r)

    if count and not count=='':
        chunks = count
    else:
        chunks = int(len(words)/text_len) + 1
#     print('分成几段', len(words), chunks)

    chunked_list = list()
    if len(results) < chunks:
        chunk_size = 1
    else:
        chunk_size = int(len(results)/chunks)+1
#     print('每段几句话', chunk_size)

    for i in range(0, len(results), chunk_size):
        chunked_list.append(results[i:i+chunk_size])
    final = []
    for r in chunked_list:
        if len(''.join(r))>5:
            final.append(''.join(r))
    return final




with open('capcut-video-editor-en-us-apple-app-review.csv', newline='', encoding='utf8') as csvfile:
    lines = csv.DictReader(csvfile)
    # count= sum(1 for line in open(csvfile))
    # count=len(list(countext))

    with open('capcut-video-editor-en-us-apple-app-review.csv',encoding='utf8') as f:
        count=sum(x.count('\n') for x in iter(partial(f.read,buffer), ''))


    with open('script.txt', 'a', encoding='utf8') as fw:
        fw.write("intro:Give your videos a professional look at zero cost|Let`s see what "+str(count)+" user saying about capcut;\r")
        # print(lines,'---------')
        for line in lines:
            print('========================s')
            mood = line['score']
            name = line['userName']
            text = line['review']
            para = split_text_into_sentences(
                text=text,
                language='en'
            )
            # //渐入背景，执行5秒
            bgani=random.choice(['bg_softIn','bg_down'])
            fw.write("setBgAni:"+bgani+" 5s;\r")
            # setBgTransform:scale(1.15, 1.15) translate(-5%, 0);//设置一个放大1.15倍，向左移动5%的变换
            # setBgFilter:blur(1px);//设置一个模糊效果

            bgeffect=['setBgTransform:scale(1.15, 1.15) translate(-5%, 0);\r','setBgFilter:blur(1px);\r']
            fw.write(random.choice(bgeffect))
            fw.write("changeBg:"+random.choice(bgfiles)+" -next;\r")
            pos=random.choice(['left','right'])
            fw.write("miniAvatar:"+random.choice(figures)+" -"+pos+" -next;\r")
            # if pos=='right':
                # time.sleep(20)
            # scores=

            animi=random.choice(['shake','upin','leftin','rightin','centerin','moveBaF'])
            fw.write("setFigAni:"+animi+" 1s -"+pos+";\r")
            if len(para) > 0:
                for i in range(len(para)):
                #     tts

                    ttsfilename='.ogg'
                    linetext=''
                    if i==0:
                        linetext=para[0]
                        # fw.write(name+':'+linetext+';'+'\r')
                    else:
                        linetext=para[i]
                    text_len=150
                    # print('------------',linetext)
                    print(len(linetext))
                    # time.sleep(2)                        
                    if len(linetext)>text_len:
                        # sces = SrcType.detect1(linetext)
                        sces=long_cjk_text2paragraph_budouX(linetext,text_len=text_len,lang='en',count='')                                    

                        print(sces)
                        # print(sces[1])
                        # sces=split_text_into_sentences(text=linetext,language='en')
                    #     sces=long_cjk_text2paragraph_budouX(linetext,text_len=text_len,lang='en',count='')
                        for sce in list(set(sces)):
                            # print(sce)
                            # print(len(sce))
                            # time.sleep(2)
                            if len(sce)>text_len:
                                ss = SrcType.detect1(sce)
                                ss=ss[1]
                                # ss=long_cjk_text2paragraph_budouX(sce,text_len=text_len,lang='en',count='')                                    
                                for s in list(set(ss)):
                                    print('=======',s,len(s))
                                    # time.sleep(10)
                                    if(len(s))>text_len:
                                        if ',' in s or '，' in s:

                                            texts=split_text_into_sentences(text=s,language='en')
                                        else:
                                            wrapper = textwrap.TextWrapper(
                                                width=text_len, break_long_words=False, replace_whitespace=False)
                                            texts = wrapper.wrap(text=s)

                                        for i in range(len(texts)):
                                            if len(text[i])>text_len:
                                                time.sleep(10)
                                                print('????????',texts[i])
                                            if len(texts[i])>3:
                                            
                                                fw.write(name+':'+texts[i]+';'+'\r')
                                    else:
                                        if len(s)>3:
                                            fw.write(name+':'+s+';'+'\r')                                        
                                            # fw.write(name+':'+s+';'+'\r')

                                # time.sleep(2)

                            else:
                                if len(sce)>3:
                                    fw.write(name+':'+sce+';'+'\r')
                    else:
                        if len(linetext)>3:

                            fw.write(name+':'+linetext+';'+'\r')                        # time.sleep(10)
                    # fw.write(linetext+';'+'\r')


#
# Object interface
#
# print(splitter.split(text='This is a paragraph. It contains several sentences. "But why," you ask?'))
# ['This is a paragraph.', 'It contains several sentences.', '"But why," you ask?']

#
# Functional interface
#
# print()
# ['This is a paragraph.', 'It contains several sentences.', '"But why," you ask?']
