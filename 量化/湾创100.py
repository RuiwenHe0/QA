# from WindPy import *
import numpy as np
import matplotlib.pyplot as plt
import cx_Oracle
import pandas as pd

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

# def get_data(): #丛wind获取员工持股计划
#     w.start()
#     info = w.wset("sectorconstituent","date=2019-07-29;windcode=980001.CNI")
#     col = ['日期','证券代码','证券名称']
#     df = pd.DataFrame(info.Data,index=col,columns=info.Codes)
#     df = df.T
#     df.to_csv('湾创100.csv',index=False,header=True,encoding='utf_8_sig')
#     w.stop()
#
# get_data()

def write_file():
    list = [1,2,3,4,5]
    df = pd.DataFrame(list)
    df = df.T
    df.to_csv("我操你妈.csv")
    df = pd.read_csv('高管增持/累计收益/平均累计收益2009.csv')
    print(df)

write_file()