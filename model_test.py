# coding: utf-8
_author = "Adien Huen"
import codecs
import os
def create_testset(testset_answer_path,testset_path):
        f = codecs.open(testset_answer_path, encoding="utf-8")
        rows = f.readlines()
        f.close()


        if not os.path.isfile(testset_path):
            os.mknod(testset_path)
            f = codecs.open(testset_path,"w", encoding="utf-8")
            for row in rows:
                row = row.replace("\n", "")
                char = row.split("	")[0]
                f.write(char+u"\n")
            f.close()
        print "create_testset ok"

def test(test_result_path,testset_answer_path):
    f_answer = codecs.open(testset_answer_path, encoding="utf-8")
    f_result = codecs.open(test_result_path, encoding="utf-8")
    data = f_answer.read()
    rows_answer = data.split("\n")
    data = f_result.read()
    rows_result = data.split("\n")
    test_num = 0
    correct_num = 0
    for i in range(rows_answer.__len__()):
        answer_items = rows_answer[i].split("	")
        result_items = rows_result[i].split("	")
        if answer_items.__len__()==2 and result_items.__len__()==2:
            test_num += 1
            if answer_items[1]==result_items[1]:
                correct_num += 1
                print answer_items[0], result_items[1], answer_items[1]
            else:
                print answer_items[0],result_items[1],answer_items[1]
    print correct_num*1.0/test_num
    f_answer.close()

if __name__ == '__main__':
    test("data/nlpcc_dataset/test_result.result","data/nlpcc_dataset/testset_answer.txt")
    # create_testset("data/nlpcc_dataset/testset_answer.txt","data/nlpcc_dataset/testset.txt")