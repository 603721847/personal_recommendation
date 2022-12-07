import operator
import os.path

import numpy as np


def load_item_vec(input_file):
    """

    :param input_file: item_vec.txt
    :return: a dict. element: key=itemId, value=[value1, value2, ..., valueDim]
    """
    if not os.path.exists(input_file):
        return {}
    line_num = 0
    fp = open(input_file, 'r')
    item_vec = {}
    for line in fp:
        if line_num == 0:
            line_num += 1
            continue
        item = line.strip().split()
        if len(item) < 129:
            continue
        itemId = item[0]
        if itemId == '</s>':
            continue
        item_vec[itemId] = list(float(ele) for ele in item[1:])
    fp.close()
    return item_vec

def cal_item_sim(item_vec, itemId, output_file, topK=10):
    """

    :param topK:
    :param item_vec: word embedding
    :param itemId:
    :param output_file: recommend result
    :return:
    """
    if itemId not in item_vec:
        return
    fix_item_vec = item_vec[itemId]
    score = {}
    for item_id in item_vec:
        if item_id == itemId:
            continue
        score[item_id] = np.dot(fix_item_vec, item_vec[item_id])/(np.linalg.norm(fix_item_vec)*np.linalg.norm(item_vec[item_id]))
    fw = open(output_file, 'w+')
    out_str = itemId + '\t'
    tmp_list = []
    for key, value in sorted(score.items(),key=operator.itemgetter(1), reverse=True)[:topK]:
        tmp_list.append(key + '_' + str(value))
    out_str += ';'.join(tmp_list)
    fw.write(out_str)
    fw.close()
def run_main(input_file, output_file):
    item_vec = load_item_vec(input_file)
    cal_item_sim(item_vec, '2858', output_file)

if __name__ == '__main__':
    item_vec = load_item_vec('item_vec.txt')
    print(len(item_vec))
    print(item_vec['2858'])
    print(len(item_vec['2858']))

    run_main("item_vec.txt", '2858_recommend.txt')


