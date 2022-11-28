import operator

from LFM.utils import get_item_info
from utils import *
from mat_utils import *

def personal_rank(graph, root, alpha, iter_num, recommend_num=10):
    """

    :param graph: user-item graph
    :param root: the user we need to recommend to
    :param alpha: the prob to go to random walk, with prob (1-alpha) go back to root
    :param iter_num:
    :param recommend_num:
    :return: a dict. key is item_id, value is pr value
    """
    rank = {point: 0 for point in graph.keys()}
    rank[root] = 1
    result = {}
    for iter_index in range(iter_num):
        tmp_rank = {point: 0 for point in graph.keys()}
        for out_point, out_dict in graph.items():
            # out_point is start point, out_dict is where could go, graph[out_point] is equal out_dict
            for inner_point, value in out_dict.items():
                tmp_rank[inner_point] += alpha * rank[out_point] / len(out_dict)
        # from the forum, we  know that each epoch only add '1-alpha' once
        tmp_rank[root] += 1 - alpha
        rank = tmp_rank
    for vertex, pr_value in sorted(rank.items(), key=operator.itemgetter(1), reverse=True):
        if len(vertex.split('_')) < 2:  # not item vertex
            continue
        if vertex in graph[root]:  # shouldn't have edge with root
            continue
        result[vertex] = pr_value
        if len(result) == recommend_num:
            break
    print(rank[root])
    return result

def personal_rank_mat(graph, root, alpha, recommend_num=10):
    m, vertex, address_dict = graph_to_m(graph)
    if root not in address_dict:
        return {}
    score_dict = {}
    recommend_list = {}
    mat_all = mat_all_point(m, vertex, alpha)
    index = address_dict[root]
    # get the col=index, of mat_all
    col_result = mat_all[:, index]
    for index in range(len(vertex)):
        point = vertex[index]
        if len(point.strip().split('_')) < 2:     # user vertex
            continue
        if point in graph[root]:
            continue
        score_dict[point] = round(col_result[index][0].sum(), 3)
    for point, pr_value in sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)[:recommend_num]:
        recommend_list[point] = pr_value
    return recommend_list

def get_one_user_recom_matrix(userID, alpha=0.8):
    graph = get_graph_from_data("../data/ratings.txt")
    recommend_list = personal_rank_mat(graph, userID, alpha)
    print("recommend result by matrix")
    item_info = get_item_info("../data/movies.txt")
    for item in recommend_list.items():
        title, genres = item_info[item[0].split('_')[1]]
        print(item[0], title, genres, item[1], sep='\t')

def get_one_user_recom(userID, alpha=0.8):
    graph = get_graph_from_data("../data/ratings.txt")
    recommend_list = personal_rank(graph, userID, alpha, 1000)
    item_info = get_item_info("../data/movies.txt")
    print("========================================================================")
    print("the movie that user ", userID, 'like is ')
    for itemID in graph[userID]:
        title, genres = item_info[itemID.split('_')[1]]
        print(itemID, title, genres)
    print("========================================================================")
    print("recommend result")
    for item in recommend_list.items():
        title, genres = item_info[item[0].split('_')[1]]
        print(item[0], title, genres, item[1], sep='\t')


if __name__ == '__main__':
    get_one_user_recom('1')
    get_one_user_recom_matrix('1')
