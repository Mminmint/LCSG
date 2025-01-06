# -*- coding: utf-8 -*-
# @Time    : 2024/11/25 19:40
# @Author  : Mminmint
# @File    : multiProcess.py
# @Software: PyCharm

import time

from simPredict import simExecute
import copy
import multiprocessing


# 多进程
def multiProcess(processNum,vehs,suggestLCs,suggestSGs):
    processes = []
    queue = multiprocessing.Queue()  # 创建一个队列用于收集结果

    # 使用多进程执行仿真
    for i in range(processNum):
        p = multiprocessing.Process(target=simExecute, args=(vehs, suggestLCs[i],suggestSGs[i],i,queue))
        processes.append(p)
        p.start()
        # print(time.time())

    # 等待所有进程完成
    for p in processes:
        p.join()

    # 收集所有仿真的返回值
    results = [queue.get() for _ in range(processNum)]
    return results


def processExecute(processNum,orgVehsInfo,suggestLCs,suggestSGs):
    results = multiProcess(processNum,orgVehsInfo,suggestLCs,suggestSGs)
    return results