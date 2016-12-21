#encoding:utf8

import math
# 计算ndcg的值


def NDCG(dcg_ranks, idcg_ranks=None):
    """
    计算NDCG的值, 如果idcg_ranks没有指定,那么为dcg_ranks的逆序值
    ndcg:
        dcg / idcg
        dcg: sum_(gain(rank) * log(2)/log(index+1)), i:[2;N], 第一个直接加
            idcg: idea dcg, 按照gain(rank)排序之后的结果.

    """
    def _gain(x):
        # gain function to increase or decrease the score
        return pow(2, x) - 1
        # return x

    if not dcg_ranks:
        return 0
    dcg_ranks = map(_gain, dcg_ranks)
    if not idcg_ranks:
        idcg_ranks = sorted(dcg_ranks, reverse=True)
    else:
        idcg_ranks = map(_gain, idcg_ranks)
    NORMALIZE = math.log(2)

    def _cal_dcg(ranks):
        if not ranks:
            return 0
        value = ranks[0] * 1.0
        for index, score in enumerate(ranks):
            if index == 0:
                continue
            value += score * NORMALIZE / math.log(2+index)
        return value

    dcg = _cal_dcg(dcg_ranks)
    idcg = _cal_dcg(idcg_ranks)
    return dcg / idcg

