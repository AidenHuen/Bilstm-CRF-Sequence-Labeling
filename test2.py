#!/usr/bin/env python
# -*- encoding: utf-8 -*-
__author__ = 'jxliu.nlper@gmail.com'
_author = "Aiden Huen"

"""
    标记文件
"""
import codecs
import yaml
import pickle
import tensorflow as tf
from load_data import load_vocs, init_data
from model import SequenceLabelingModel
import os
from tqdm import tqdm

import codecs
import yaml
import pickle
import tensorflow as tf
from load_data import load_vocs, init_data
from model import SequenceLabelingModel
import os

def tagging():
    # 加载配置文件
    with open('./config.yml') as file_config:
        config = yaml.load(file_config)

    feature_names = config['model_params']['feature_names']  # 读取特征名
    use_char_feature = config['model_params']['use_char_feature']

    # 初始化embedding shape, dropouts, 预训练的embedding也在这里初始化)
    feature_weight_shape_dict, feature_weight_dropout_dict, \
        feature_init_weight_dict = dict(), dict(), dict()
    for feature_name in feature_names:
        feature_weight_shape_dict[feature_name] = \
            config['model_params']['embed_params'][feature_name]['shape']
        feature_weight_dropout_dict[feature_name] = \
            config['model_params']['embed_params'][feature_name]['dropout_rate']
        path_pre_train = config['model_params']['embed_params'][feature_name]['path']
        if path_pre_train:  # 如果特证包含与训练embedding
            with open(path_pre_train, 'rb') as file_r:
                feature_init_weight_dict[feature_name] = pickle.load(file_r)

    # char embedding shape
    if use_char_feature:
        feature_weight_shape_dict['char'] = \
            config['model_params']['embed_params']['char']['shape']
        conv_filter_len_list = config['model_params']['conv_filter_len_list']
        conv_filter_size_list = config['model_params']['conv_filter_size_list']
    else:
        conv_filter_len_list = None
        conv_filter_size_list = None

    # 加载vocs
    print "加载字典......"
    path_vocs = []
    if use_char_feature:
        path_vocs.append(config['data_params']['voc_params']['char']['path'])
    for feature_name in feature_names:
        path_vocs.append(config['data_params']['voc_params'][feature_name]['path'])
    path_vocs.append(config['data_params']['voc_params']['label']['path'])
    vocs = load_vocs(path_vocs)


    # 加载数据
    print "加载测试集......"
    sep_str = config['data_params']['sep']

    assert sep_str in ['table', 'space']
    sep = '\t' if sep_str == 'table' else ' '
    max_len = config['model_params']['sequence_length']
    word_len = config['model_params']['word_length']
    data_dict = init_data(
        path=config['data_params']['path_test'], feature_names=feature_names, sep=sep,
        vocs=vocs, max_len=max_len, model='test', use_char_feature=use_char_feature,
        word_len=word_len)

    # 加载模型
    model = SequenceLabelingModel(
        sequence_length=config['model_params']['sequence_length'],
        nb_classes=config['model_params']['nb_classes'],
        nb_hidden=config['model_params']['bilstm_params']['num_units'],
        num_layers=config['model_params']['bilstm_params']['num_layers'],
        feature_weight_shape_dict=feature_weight_shape_dict,
        feature_init_weight_dict=feature_init_weight_dict,
        feature_weight_dropout_dict=feature_weight_dropout_dict,
        dropout_rate=config['model_params']['dropout_rate'],
        nb_epoch=config['model_params']['nb_epoch'], feature_names=feature_names,
        batch_size=config['model_params']['batch_size'],
        train_max_patience=config['model_params']['max_patience'],
        use_crf=config['model_params']['use_crf'],
        l2_rate=config['model_params']['l2_rate'],
        rnn_unit=config['model_params']['rnn_unit'],
        learning_rate=config['model_params']['learning_rate'],
        use_char_feature=use_char_feature,
        conv_filter_size_list=conv_filter_size_list,
        conv_filter_len_list=conv_filter_len_list,
        word_length=word_len,
        path_model=config['model_params']['path_model'])
    saver = tf.train.Saver()
    saver.restore(model.sess, config['model_params']['path_model'])

    # 标记
    viterbi_sequences = model.predict(data_dict)

    # # 写入文件
    label_voc = dict()
    for key in vocs[-1]:
        label_voc[vocs[-1][key]] = key
    with codecs.open(config['data_params']['path_test'], 'r', encoding='utf-8') as file_r:
        sentences = file_r.read().strip().split('\n\n')
    file_result = codecs.open(
        config['data_params']['path_result'], 'w', encoding='utf-8')
    for i, sentence in enumerate(sentences):
        for j, item in enumerate(sentence.split('\n')):
            if j < len(viterbi_sequences[i]):
                file_result.write('%s\t%s\n' % (item, label_voc[viterbi_sequences[i][j]]))
            else:
                file_result.write('%s\tO\n' % item)
        file_result.write('\n')

    file_result.close()

def create_testset():
    """
    生成待标注测试集文件
    :param testset_answer_path: 已标注测试集路径
    :param testset_path:    待标注测试集路径
    """
    with open('./config.yml') as file_config:
        config = yaml.load(file_config)

    f = codecs.open(config["data_params"]["path_answer"], encoding="utf-8")
    rows = f.readlines()
    f.close()


    if not os.path.isfile(config["data_params"]["path_test"]):
        os.mknod(config["data_params"]["path_test"])

    f = codecs.open(config["data_params"]["path_test"], "w", encoding="utf-8")
    for row in rows:
        row = row.replace("\n", "")
        # print row
        items = row.split("\t")
        # print items

        if len(items) == 1:
            f.write(items[0] + u"\n")
        else:

            row = "\t".join(items[0:len(items)-1])
            f.write(row+u"\n")
    f.close()
    print "create_testset ok"

def get_precision():
    """
    精度计算,基于人名
    """
    with open('./config.yml') as file_config:
        config = yaml.load(file_config)
    f_answer = codecs.open(config["data_params"]["path_answer"], encoding="utf-8")
    f_result = codecs.open(config["data_params"]["path_result"], encoding="utf-8")
    data = f_answer.read()
    f_answer.close()
    rows_answer = data.split("\n")
    items_answer = [[i.split("	")[0], i.split("	")[len(i.split("	"))-1]] for i in rows_answer]
    data = f_result.read()
    f_result.close()
    rows_result = data.split("\n")
    items_result = [[i.split("	")[0], i.split("	")[len(i.split("	")) - 1]] for i in rows_result]
    precision_num = 0.0
    recall_num = 0.0
    correct_num = 0.0
    for items in items_result:
        # print items[0],items[1]
        try:
            if items[1][0] == "B" and items[1][2:]=="nrn":
                precision_num += 1
        except:
            pass
    for items in items_answer:
        # print items
        try:
            if items[1][0] == "B" and items[1][2:]=="nrn":
                recall_num += 1
        except:
            pass
    i = 0
    while i < items_answer.__len__():
        if items_result[i][1]!="" and items_answer[i][1]!="":
            if items_result[i][1][0] == "B" and items_result[i][1][0] == items_answer[i][1][0]:
                j = i
                while j<items_answer.__len__():

                    if items_answer[j][1][0] != "E":
                        j+=1
                    else:
                        break
                if items_result[j][1][0] == "E" and items_answer[j][1][2:]=="nrn":
                    # print items_answer[j][1], items_result[j][1]
                    correct_num += 1
                    i = j
        i += 1
    p = correct_num/precision_num
    r = correct_num/recall_num

    print("nrn")
    print ("p:")
    print(p)
    print ("r:")
    print (r)
    print ("f:")
    print(2*p*r/(p+r))

# if __name__ == '__main__':
#     create_testset()
#     tagging()  # 标记测试集
#     get_precision()
    # get_indicator()