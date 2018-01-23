# coding:utf-8
import jieba
import sys

reload(sys)

"""
生成word2vec训练文本格式
"""

class text_class(object):

    def __init__(self, input_path,output_path):
        self.input = input_path
        self.out_put = output_path

    def transfer_text(self):
        """
        将nlpcc标记集转换为word2vec训练集
        :return: None
        """
        list = []
        result = []
        count = {}
        with open(self.input) as f:
            for i in f.readlines():
                i = i.replace('\n', '')
                i = i.split("	")
                k = i[0]
                if(k == "\n"):
                    continue
                else:
                    list.append(k)
        # 初始化
        for k in list:
            count[k] = 0

        # 统计单个字出现次数
        for i in list:
            count[i]+=1

        # 对低频词进行更改
        kg = " "
        new_list = []
        for i in list:
            # if(count[i]<3):
            #     i = "❤"
            new_list.append(i + " ")
        # print kg.join(new_list)
        with open(self.out_put,"a")as po:
            po.write("".join(new_list))
        print "done!!!"

    #text2 这是一整段的文字的分割
    def get_text2(self):
        list = []
        result = []
        count = {}
        with open(self.input) as f:
            for i in f.readlines():
                i.replace('\t', '').replace('\n', '')
                i = i.split(" ")
                for word in i:
                    list.append(word)

        # 初始化
        for k in list:
            count[k] = 0

        # 统计单个字出现次数
        for i in list:
            count[i] += 1

        # 对低频词进行更改
        for i in list:
            # if (count[i] < 3):
            #     i = "❤"
            with open(self.out_put, "a")as po:
                print i
                po.write(i + " ")

        print "done！！！"

if __name__ == '__main__':

    p = text_class("data/train_set.txt", "data/nlpcc_train.txt")
    p.transfer_text()

