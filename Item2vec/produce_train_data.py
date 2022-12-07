# coding=utf-8
import os.path


def produce_train_data(input_file, out_file, score_threshold=4.0):
    """
    after process, we can get a file that each line is consist of a sequence itemId that someone likes
    :param input_file: ratings.txt
    :param out_file:
    :param score_threshold:
    :return:
    """
    if not os.path.exists(input_file):
        return
    fp = open(input_file, 'r', encoding='utf-8')
    line_num = 0
    record = {}
    for line in fp:
        if line_num == 0:
            line_num += 1
            continue
        item = line.strip().split(',')
        if len(item) < 4:
            continue
        userId, itemId, rating = item[0], item[1], float(item[2])
        if rating < score_threshold:
            continue
        if userId not in record.keys():
            record[userId] = []
        record[userId].append(itemId)
    fp.close()
    fw = open(out_file, 'w+', encoding='utf-8')
    for userId in record:
        fw.write(" ".join(record[userId]) + '\n')
    fw.close()


if __name__ == '__main__':
    produce_train_data("../data/ratings.txt", 'train.txt')
