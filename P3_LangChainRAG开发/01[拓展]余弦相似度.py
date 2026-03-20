import numpy as np

def get_dot(vec_a,vec_b):
    #计算两个向量的点积，两个向量同维度数字乘积之和
    if len(vec_a) != len(vec_b):
        raise ValueError("两个向量必须维度数量相同")
    dot_sum = 0
    for a,b in zip(vec_a,vec_b):
        dot_sum += a*b
    return dot_sum

def get_norm(vec):
    #计算单个向量的模长，对向量的每个数字求平方再求和再开根号
    sum_square = 0
    for v in vec:
        sum_square += v*v

    #numpy sqrt函数完成开根号
    return np.sqrt(sum_square)

def cosine_similarity(vec_a,vec_b):
    """余弦相似度：两个向量的点积除以两个向量模长乘积"""
    result = get_dot(vec_a,vec_b)/(get_norm(vec_a)*get_norm(vec_b))
    return result

if __name__ == "__main__":
    vec_a = [0.5,0.5]
    vec_b = [0.7,0.7]
    vec_c = [0.7,0.5]
    vec_d = [-0.6,-0.5]

    print("ab:",cosine_similarity(vec_a,vec_b))
    print("ac:",cosine_similarity(vec_a,vec_c))
    print("ad:",cosine_similarity(vec_a,vec_d))