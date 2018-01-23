# coding:utf-8
from get_text import text_class
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
from gensim.models import word2vec
from gensim.models import Word2Vec
import logging, gensim, os

"""
word2vec
"""


def skip_gram_train(tran_path, save_path, dim_size, min_count, window):
    """
    基于skip gram模型的embedding训练
    :param tran_path: 训练集路径
    :param save_path: embedding保存路径
    :param dim_size: 维度大小
    :param dim_count: 最少字符频率
    :param window: 窗口大小
    :return: None
    """
    word_bag = []
    sentences=word2vec.Text8Corpus(tran_path)

    model = Word2Vec(sentences, sg=1, size=dim_size,  window=window,  min_count=min_count,  negative=0, sample=0.001,
                     hs=1)


    print "model has ok"
    #去重
    for i in sentences:
        for word in i:
            word_bag.append(word)
    word_bag = set(word_bag)
    with open(save_path, "a")as po:
        po.write(str(word_bag.__len__()))
        po.write(" ")
        po.write(str(dim_size))
        po.write("\n")
        po.close()
    for k in word_bag:
        array = model[k]
        list_ar = array.tolist()
        print k, list_ar

        for i in range(0, list_ar.__len__()):
            list_ar[i] = str(list_ar[i])

        with open(save_path, "a")as pi:
            pi.write(k )
            pi.write(" ")
            pi.write(" ".join(list_ar))
            pi.write("\n")
    print "ok"


if __name__ == '__main__':
    # 在这里输入文档名字,输入文档 和 转换格式后的文档
    p = text_class("data/origin/nlpcc_all.txt", "data/train_text/nlpcc_all.txt")
    # #调用方法一
    p.transfer_text()
    skip_gram_train("data/train_text/nlpcc_all.txt", "data/char_embed/nlpcc_embed_d200_w9_all", 200, 0, 9)



