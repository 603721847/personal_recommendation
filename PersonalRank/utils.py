import os.path


def get_graph_from_data(input_file, score_threshold=4.0):
    """
    :param input_file:
    :param score_threshold: threshold to judge user whether like the movie or not
    :return: a dict. element:
        key is the vertex
        {
            userA:{itemb:1, itemc:1},
            itemb:{userA:1}
        }
    """
    if not os.path.exists(input_file):
        return {}
    line_num = 0
    graph_dict = {}
    fp = open(input_file, 'r', encoding='utf-8')
    for line in fp:
        if line_num == 0:
            line_num += 1
            continue
        item = line.strip().split(',')
        if len(item) < 3:
            continue
        user_id, item_id, rating = item[0], 'item_' + item[1], float(item[2])  # inorder to margin user and item
        if rating < score_threshold:
            continue
        if user_id not in graph_dict:
            graph_dict[user_id] = {}
        if item_id not in graph_dict:
            graph_dict[item_id] = {}
        graph_dict[user_id][item_id] = 1
        graph_dict[item_id][user_id] = 1
    return graph_dict


if __name__ == '__main__':
    graph_dict = get_graph_from_data("../data/ratings.txt")
    print(graph_dict['item_1193'])
