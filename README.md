

# Bilstm-CRF-Sequence-Labeling
An easy-to-use sequence labeling toolkit, implemented the LSTM+\[CNN\]+CRF model in tensorflow. the source repo is from https://github.com/liu-nlper/NER-LSTM-CRF . you can directly use the model in this repo or use your own train set to train a new model.<br>

##Statement
repo中的已有的模型基于nlpcc2015中文POS集进行训练,可直接用于中文词性标注和分词,运行`test.py`输出标注结果.通过配置`config.yml`，实现模型训练和测试,下面详细介绍模型训练过程<br>

### 1.1 预处理
    $ python/python3 preprocessing.py
预处理后，会得到各个特征的item数以及label数，并自动修改`config.yml`文件中各个feature的`shape`参数，以及`nb_classes`参数；

句子的最大长度参数`sequence_length`由参数`sequence_len_pt`控制，默认为`98`，即计算所得的句子长度`sequence_length`覆盖了98%的实例，可根据实际情况作调整；

需要注意的是，若提供了预训练的embedding向量，则特征embedding的维度以预训练的向量维度为准，若没有提供预训练的向量，则第一列的特征向量维度默认为64，其余特征为32，这里可以根据实际情况进行调整。

### 1.2 训练模型

训练模型：根据需要调整其余参数，其中dev_size表示开发集占训练集的比例（默认值为0.1），并运行：

    $ python/python3 train.py

### 1.3 测试模型
测试模型：`config.yml`中修改相应的`path_test`和`path_result`和`path_answer`，并运行：

    $ python/python3 test.py

### 1.4 参数说明

|  | 参数 |说明  |
| ------------ | ------------ | ------------ |
|1|rnn_unit| str，\['lstm', 'gru'\]，模型中使用哪种单元，用户设置，默认值`lstm`|
|2|num_units| int，bilstm/bigru单元数，用户设置，默认值`256`|
|3|num_layers| int，bilstm/bigru层数，用户设置，默认值`1`|
|4|rnn_dropout| float，lstm/gru层的dropout值，用户设置，默认值`0.2`|
|5|use_crf| bool，是否使用crf层，用户设置，默认值`true`|
|6|use_char_feature| bool，是否使用字符层面特征（针对英文），用户设置，默认值`false`|
|7|learning_rate| float，学习率，用户设置，默认值`0.001`|
|8|dropout_rate| float，bilstm/bigru输出与全连接层之间，用户设置，默认值`0.5`|
|9|l2_rate| float，加在全连接层权重上，用户设置，默认值`0.001`|
|10|clip:| None or int, 梯度裁剪，用户设置，默认值`10`|
|11|dev_size| float between (0, 1)，训练集中划分出的开发集的比例，shuffle之后再划分，用户设置，默认值`0.2`|
|12|sequence_len_pt|int，句子长度百分数，用于设定句子最大长度，用户设置，默认值`98`|
|13|sequence_length| int，句子最大长度，由参数`sequence_len_pt`计算出，无需设置|
|14|word_len_pt|int，单词长度百分数，用于设定单词最大长度，只有在`use_char_feature`设为`true`时才会使用，用户设置，默认值`95`|
|15|word_length| int，单词最大长度，由参数`word_len_pt`计算出
|16|nb_classes| int，标签数，自动计算，无需设置|
|17|batch_size| int，batch size，用户设置，默认值为`64`|
|18|nb_epoch| int，迭代次数，用户设置|
|19|max_patience| int，最大耐心值，即在开发集上的表现累计max_patience次没有提升时，训练即终止，用户设置，默认值`5`|
|20|path_model| str，模型存放路径，用户设置，默认值值`./Model/best_model`|
|21|sep| str，\['table', 'space'\]，表示特征之间的分隔符，用户设置，默认值`table`|
|22|conv_filter_size_list|list，当使用`char feature`时，卷积核的数量，用户设定，默认值`[8, 8, 8, 8, 8]`|
|23|conv_filter_len_list|list，当使用`char feature`时，卷积核的尺寸，用户设定，默认值`[1, 2, 3, 4, 5]`|
|24|conv_dropout|卷积层的dropout rate|
|25|Other parameters|......|

### 针对nlpcc2015词性标注任务
训练集为`data/nlpcc_dataset/train.txt`<br>
测试集为`data/nlpcc_dataset/testset.txt`<br>
embedding集存于`data/envedding/.txt`<br>
测试集标注结果存至`data/nlpcc_dataset/test_result.result`<br>
测试集答案为`data/nlpcc_dataset/testset_answer.txt`<br>
运行 'test.py' 对测试集进行标注，并计算准确率

## 2. Requirements
- numpy
- tensorflow 1.4
- pickle
- tqdm
- yaml

