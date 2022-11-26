import numpy as np
from utils import *


def init_vec(dim):
    return np.random.randn(dim)


def model_predict(user_vec, item_vec):
    """

    :param user_vec:
    :param item_vec:
    :return: cosine similarity, the scale is [-1, 1]
    """
    res = np.dot(user_vec, item_vec) / (np.linalg.norm(user_vec) * np.linalg.norm(item_vec))
    return res


def lfm_train(train_data, dim=50, alpha=0.01, lr=0.1, epoch=1):
    """

    :param train_data:
    :param dim:  the dimension of the latent vector
    :param alpha: regularization hyper
    :param lr: learning rate
    :param epoch: the num of train epoch
    :return:
    """
    user_vec = {}
    item_vec = {}
    for step_index in range(epoch):
        for data_instance in train_data:
            userId, itemId, label = data_instance
            if userId not in user_vec:
                user_vec[userId] = init_vec(dim)
            if itemId not in item_vec:
                item_vec[itemId] = init_vec(dim)
            # iter
            delta = label - model_predict(user_vec[userId], item_vec[itemId])
            for index in range(dim):
                user_vec[userId][index] += lr * (delta * item_vec[itemId][index] - alpha * user_vec[userId][index])
                item_vec[itemId][index] += lr * (delta * user_vec[userId][index] - alpha * item_vec[itemId][index])
    return user_vec, item_vec


def give_recom_result(user_vec, item_vec, userId):
    """
    use the result of LFM model to find the recommend result corresponding to userId
    :param user_vec:
    :param item_vec:
    :param userId:
    :return: a list, element:(itemID, recommend_score)
    """
    if userId not in user_vec.keys():
        return []
    record = {}
    recom_list = []
    fix_num = 5
    user_vector = user_vec[userId]
    for itemID in item_vec:
        item_vector = item_vec[itemID]
        similarity = model_predict(user_vector, item_vector)
        record[itemID] = similarity
    for item in sorted(record.items(), key=lambda element: element[1], reverse=True)[:fix_num]:
        itemID, score = item[0], round(item[1], 3)
        recom_list.append((itemID, score))
    return recom_list


def analysis_recom_result(train_data, userID, recom_result):
    """

    :param train_data:
    :param userID:
    :param recom_result: the recommend result that lfm gives
    :return:
    """
    item_info = get_item_info('../data/movies.txt')
    print("the history that the user like")
    for data_instance in train_data:
        userID_instance, itemID, label = data_instance
        if userID_instance == userID and label == 1:
            print(item_info[itemID])
    print("recommend result")
    for item in recom_result:
        print(item_info[item[0]], item[1])


def model_train_process():
    """
    train LFM model
    :return:
    """
    train_data = get_train_data("../data/ratings.txt")
    user_vec, item_vec = lfm_train(train_data)
    recom_result = give_recom_result(user_vec, item_vec, "11")
    analysis_recom_result(train_data, "11", recom_result)


if __name__ == '__main__':
    model_train_process()
