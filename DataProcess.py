# coding: utf-8
_author = "Aiden Huen"
import codecs

def nerCount():
    path = "./testset_answer.txt"
    # path = "./film/trainset_df.txt"
    # path = "./film/testset_answer.txt"
    # path = "./film_random/testset_answer.txt"
    f = codecs.open(path,encoding="utf-8")
    rows = f.read()
    rows = rows.split("\n")
    nrn = 0
    nr = 0
    nrf = 0
    for row in rows:
        items = row.split("	")

        if "B-nrn" == items[items.__len__()-1]:
            nrn+=1
            print(items[items.__len__()-1])
        if "B-nr" == items[items.__len__()-1]:
            nr+=1
        if "B-nrf" == items[items.__len__()-1]:
            nrf+=1
    print("nrn:"+str(nrn))
    print("nrf:"+str(nrf))
    print("nr:"+str(nr))

def feature_filter():

    select_index = [0, 10]
    select_index = [0,1,2,3,4,5,6,7,10]
    select_index = [0,8,9,10]
    r_path = "./film_random/testset_answer.txt"
    w_path = "./film_random/testset_answer_3.txt"

    f = codecs.open(r_path, encoding="utf-8")
    rows = f.read()
    rows = rows.split("\n")
    f.close()
    f = codecs.open(w_path, mode="w", encoding="utf-8")
    for row in rows:
        items = row.split("\t")
        row = []
        if items.__len__() != 1:
            for index in select_index:
                row.append(items[index])
            f.write("\t".join(row) + "\n")
        else:
            f.write("" + "\n")

def get_random_review():
    f = codecs.open("./film_comment.txt",encoding="utf-8")
    data = f.read()
    f.close()
    comments = data.split("\n\n")
    trainset = []
    testset  =[]
    import random
    for c in comments:
        if random.random()>=0.8:
            testset.append(c)
        else:
            trainset.append(c)
    print(trainset.__len__())
    print(testset.__len__())
    f = codecs.open("./testset_answer.txt",mode="w",encoding="utf-8")
    data = "\n\n".join(testset)
    f.write(data)
    f.close()
    f = codecs.open("./trainset.txt",mode="w",encoding="utf-8")
    data = "\n\n".join(trainset)
    f.write(data)
    f.close()

def get_register_name():
    path_eng_name = "./data/English_Cn_Name_Corpus（48W）.txt"
    path_cn_name = "./data/Chinese_Names_Corpus（120W）.txt"
    path_train = "./data/film/trainset_1.txt"

    f = codecs.open(path_cn_name, encoding="utf-8")
    data = f.read()
    f.close()
    names = {}
    cn_name = data.split("\r\n")
    for name in cn_name:
        names[name] = 1
    f = codecs.open(path_eng_name, encoding="utf-8")
    data = f.read()
    f.close()
    eng_name = data.split("\n")
    for name in eng_name:
        names[name] = 1
    # for name in names:
    #     print(name)

    f = codecs.open(path_train, encoding="utf-8")
    data = f.read()
    rows = data.split("\n")

    items = [row.split("	")for row in rows]
    for i in range(len(items)):
        # print items[i]
        if items[i].__len__() > 1:
            try:
                if items[i][1][0] == "B":
                    name = ""
                    name += items[i][0]
                    j = i+1
                    while(j<items.__len__()):
                        if items[j][1][0] == "M":
                            name += items[j][0]
                        elif items[j][1][0] == "E":
                            name += items[j][0]
                            # print name
                            names[name] = 1
                            break
                        elif items[j][1] == "W":
                            if name.__len__() > 2:
                                # print name
                                names[name] = 1
                                break
                        j += 1

            except:
                pass
    return names
def count_unregister_name():
    names = get_register_name()

    path_test = "./data/film/testset_answer_1.txt"
    test_names = []
    f = codecs.open(path_test,encoding="utf-8")
    data = f.read()
    rows = data.split("\n")
    name = ""
    items = [row.split("	")for row in rows]
    for i in range(len(items)):
        # print items[i]
        if items[i].__len__() > 1:
            try:
                if items[i][1][0] == "B":
                    name = ""
                    name += items[i][0]
                    j = i+1
                    while(j<items.__len__()):
                        if items[j][1][0] == "M":
                            name += items[j][0]
                        elif items[j][1][0] == "E":
                            name += items[j][0]

                            test_names.append(name)
                            break
                        elif items[j][1] == "W":
                            if name.__len__() > 2:

                                test_names.append(name)
                                break
                        j += 1

            except:
                pass

    num = 0
    all = 0

    for name in test_names:
        try:
            names[name]+=1
            all += 1
        except:
            # print name
            num += 1
            all += 1
    print(names.__len__())
    print(num)
    print(all)
    print float(num)/all
    return names

# count_unregister_name()