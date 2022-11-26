import os


def get_item_info(input_file):
    """
    read the movies file and return a dict with the key is movieId, and the value is a list contain title and genres
    :param input_file: movies file
    :return:
        key: itemId
        value: [title, genres]
    """
    if not os.path.exists(input_file):
        return {}
    item_info = {}
    lineNum = 0
    fp = open(input_file, 'r', encoding='utf-8')
    for line in fp:
        if lineNum == 0:
            lineNum += 1
            continue
        # read per line and get movieId, title, genres
        item = line.strip().split(',')
        if len(item) < 3:
            continue
        elif len(item) == 3:
            itemId, title, genres = item[0], item[1], item[2]
        elif len(item) > 3:
            itemId = item[0]
            genres = item[-1]
            title = ','.join(item[1:-1])
        item_info[itemId] = [title, genres]
    fp.close()
    return item_info


def get_avg_score(input_file):
    """
    read the ratings.txt, and get each movie's avg score
    :param input_file: ratings.txt
    :return:
    """
    if not os.path.exists(input_file):
        return {}
    lineNum = 0
    record_dict = {}  # key is movieId, value is a list with appearance times and total score
    score_dict = {}  # key is movieId, value is corresponding avg score
    fp = open(input_file, 'r', encoding='utf-8')
    for line in fp:
        if lineNum == 0:
            lineNum += 1
            continue
        item = line.strip().split(',')
        userId, movieId, rating = item[0], item[1], float(item[2])
        if movieId not in record_dict:
            record_dict[movieId] = [0, 0]
        record_dict[movieId][0] += 1
        record_dict[movieId][1] += rating
    fp.close()
    for movieId in record_dict.keys():
        score_dict[movieId] = record_dict[movieId][1] / record_dict[movieId][0]
    return score_dict


def get_train_data(input_file, score_threshold=4):
    """
    if rating >= 4, label=1, else label = 0
    construct a train data, and the positive sample num is equal to the negative sample.

    In general, the num of positive sample is more than negative sample, so when we do negative sampling, we need to
    consider the avg score of the negative movieId.

    :param score_threshold:
    :param input_file:
    :return: list, element:[userId, movieId, label]
    """
    if not os.path.exists(input_file):
        return []
    score_dict = get_avg_score(input_file)
    neg_dict = {}
    pos_dict = {}
    lineNum = 0
    train_data = []
    fp = open(input_file, 'r', encoding='utf-8')
    for line in fp:
        if lineNum == 0:
            lineNum += 1
            continue
        item = line.strip().split(',')
        if len(item) < 4:
            continue
        userId, movieId, rating = item[0], item[1], float(item[2])
        if userId not in pos_dict:
            pos_dict[userId] = []
        if userId not in neg_dict:
            neg_dict[userId] = []
        if rating >= score_threshold:
            pos_dict[userId].append((movieId, 1))
        else:
            score = score_dict.get(movieId, 0)  # avg score corresponding to the movie
            neg_dict[userId].append((movieId, score))
    fp.close()

    # construct sample
    for userId in pos_dict.keys():
        data_num = min(len(pos_dict[userId]), len(neg_dict[userId]))
        if data_num == 0:
            continue
        # add positive sample
        train_data += [(userId, movieId, label) for movieId, label in pos_dict[userId][:data_num]]
        # add negative sample, we need to rank negative sample with it's avg score
        sorted_neg_list = sorted(neg_dict[userId], key=lambda element: element[1], reverse=True)[:data_num]
        train_data += [(userId, movieId, 0) for movieId, _ in sorted_neg_list]
    return train_data


if __name__ == '__main__':
    item_dict = get_item_info('../data/movies.txt')
    print(len(item_dict))
    print(item_dict["11"])

    avg_dict = get_avg_score("../data/ratings.txt")
    print(avg_dict['1193'])

    train_data = get_train_data("../data/ratings.txt")
    print(train_data)
