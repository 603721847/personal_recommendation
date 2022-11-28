"""
matrix form can get each user's recommend result
"""
from scipy.sparse import coo_matrix
import numpy as np

from PersonalRank.utils import get_graph_from_data


def graph_to_m(graph):
    """
    :param graph: two parts graph
    :return:
        a sparse matrix: M
        a list: vertex
        a dict: key is userID, value is index corresponding to the userID
    """
    vertex = list(graph.keys())  # a list
    address_dict = {}  # key is userID, value is index
    row = []
    col = []
    data = []
    for index in range(len(vertex)):
        address_dict[vertex[index]] = index
    for userID in graph:
        weight = round(1 / len(graph[userID]), 3)  # 1/out(i)
        row_index = address_dict[userID]
        for itemID in graph[userID]:
            col_index = address_dict[itemID]
            # add to list
            row.append(row_index)
            col.append(col_index)
            data.append(weight)
    return coo_matrix((data, (row, col)), shape=(len(vertex), len(vertex))).toarray(), vertex, address_dict

def mat_all_point(m_mat, vertex, alpha):
    """
    get (E-alpha*m_mat).T
    :param m_mat:
    :param vertex:
    :param alpha: the prob of random walk
    :return:
        a sparse matrix
    """
    # inorder to save memory, init E user sparse matrix
    vertex_num = len(vertex)
    row = []
    col = []
    data = []
    for index in range(vertex_num):
        row.append(index)
        col.append(index)
        data.append(1)
    sparseE = coo_matrix((data, (row, col)), shape=(vertex_num, vertex_num))
    return np.linalg.inv(sparseE - alpha*m_mat.transpose())

if __name__ == '__main__':
    graph = get_graph_from_data("../data/log.txt")
    m, vertex, address_dict = graph_to_m(graph)
    print(address_dict)
    print(m)
    print(mat_all_point(m, vertex, 0.8))
