import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cx_Oracle
import random

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

# def get_index(): #获取指数信息


def update_zz800_cons():#获取中证800历史成分股
    conn = cx_Oracle.connect('wind/wind@172.16.50.232/dfcf')
    cursor = conn.cursor()
    # date = pd.read_csv(open('cons/中证800.csv')).iloc[-1]['date'].replace('-', '')
    date = '20100101'
    cursor.execute("select F3_1807, F16_1090, OB_OBJECT_NAME_1090, F4_1807 from TB_OBJECT_1807,TB_OBJECT_1090 where F1_1807='S24133' and F2_1807=F2_1090 and F3_1807>{0}".format(date))
    df = pd.DataFrame(cursor.fetchall(), columns=['date', 'code', 'name', 'weight'])
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(['date', 'code']).to_csv('cons/中证800.csv', mode='a', header=False, index=False, encoding='utf_8_sig')

def update_zz500_cons():
    conn = cx_Oracle.connect('wind/wind@172.16.50.232/dfcf')
    cursor = conn.cursor()
    # date = pd.read_csv(open('cons/中证500.csv')).iloc[-1]['date'].replace('-', '')
    date = '20100101'
    cursor.execute("select F3_1807, F16_1090, OB_OBJECT_NAME_1090, F4_1807 from TB_OBJECT_1807,TB_OBJECT_1090 where F1_1807='S24125' and F2_1807=F2_1090 and F3_1807>{0}".format(date))
    df = pd.DataFrame(cursor.fetchall(), columns=['date', 'code', 'name', 'weight'])
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(['date', 'code']).to_csv('cons/中证500.csv', mode='a', header=False, index=False,encoding='utf_8_sig')

def update_zz1000_cons():
    conn = cx_Oracle.connect('wind/wind@172.16.50.232/dfcf')
    cursor = conn.cursor()
    # date = pd.read_csv(open('cons/中证1000.csv')).iloc[-1]['date'].replace('-', '')
    date = '20100101'
    cursor.execute("select F3_1807, F16_1090, OB_OBJECT_NAME_1090, F4_1807 from TB_OBJECT_1807,TB_OBJECT_1090 where F1_1807='S5096626' and F2_1807=F2_1090 and F3_1807>{0}".format(date))
    df = pd.DataFrame(cursor.fetchall(), columns=['date', 'code', 'name', 'weight'])
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(['date', 'code']).to_csv('cons/中证1000.csv', mode='a', header=False, index=False,encoding='utf_8_sig')

def update_hs300_cons():
    conn = cx_Oracle.connect('wind/wind@172.16.50.232/dfcf')
    cursor = conn.cursor()
    # date = pd.read_csv(open('cons/沪深300.csv')).iloc[-1]['date'].replace('-', '')
    date = '20100101'
    cursor.execute("select F3_1807, F16_1090, OB_OBJECT_NAME_1090, F4_1807 from TB_OBJECT_1807,TB_OBJECT_1090 where F1_1807='S12426' and F2_1807=F2_1090 and F3_1807>{0}".format(date))
    df = pd.DataFrame(cursor.fetchall(), columns=['date', 'code', 'name', 'weight'])
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(['date', 'code']).to_csv('cons/沪深300.csv', mode='a', header=False, index=False,encoding='utf_8_sig')

def find_stock(year,option):
    dataframe = pd.read_csv('cons/{0}.csv'.format(option), names=['date', 'code', 'name', 'weight'], encoding='utf_8_sig')
    found=[]
    df = pd.read_csv('hq/业绩超预期/业绩超预期{0}.csv'.format(year),header='infer',encoding='utf_8_sig')
    date = df['实际净利润公告日期'].values
    tradecode= df['交易代码'].values
    unique = dataframe.drop_duplicates(subset=['date'], keep='first', inplace=False)
    unique_date = unique['date'].values
    for i in range(len(df)):
        if date[i] in unique_date:
            if tradecode[i] in dataframe.loc[dataframe['date']==date[i],'code'].values:
                list = dataframe.loc[(dataframe['date'] == date[i])&(dataframe['code'] == tradecode[i]),('date','code','name')].values[0]
                sub_list=[date[i]]
                [sub_list.append(list[i]) for i in range(1,len(list))]
                found.append(sub_list)
        elif tradecode[i] in dataframe['code'].values:
            list = dataframe.loc[(dataframe['code'] == tradecode[i])].values
            name = list[0][2]
            month = [list[i][0][:7] for i in range(len(list))]
            if date[i][:7] in month:
                sub_list=[date[i],tradecode[i],name]
                found.append(sub_list)
    found_df=pd.DataFrame(found,index=['{0}'.format(year) for i in range(len(found))],columns=['财报公告日','交易代码','公司名称'])
    result = [[len(df),len(found_df), len(found_df)/len(df)]]
    result_pd = pd.DataFrame(result,index=['{0}'.format(year)],columns=['总共超预期数量','{0}成分股数量'.format(option),'比重'])
    found_df.to_csv('业绩超预期{0}成分股（十年）.csv'.format(option),mode='a',index=True,header=False,encoding='utf_8_sig')
    result_pd.to_csv('业绩超预期{0}成分股比重（十年）.csv'.format(option),mode='a',index=True,header=False,encoding='utf_8_sig')

def graph():
    option = ['沪深300','中证500','中证800','中证1000']
    plt.figure(1,figsize=(15,15))
    for i in range(len(option)):
        df = pd.read_csv('业绩超预期{0}成分股比重（十年）.csv'.format(option[i]),names=['年份','总共超预期数量','{0}成分股数量'.format(option[i]),'比重'],encoding='utf_8_sig')
        sub_df = df.loc[df['比重']!=0]
        year = sub_df['年份'].values
        weight = sub_df['比重'].values
        total = sum(sub_df['{0}成分股数量'.format(option[i])].values)/sum(sub_df['总共超预期数量'])
        plt.subplot(221+i)
        plt.bar(np.append(year,['合计']),np.append(weight,[total]))
        plt.title('业绩超预期{0}成分股占比统计'.format(option[i]))
        # plt.show()
    plt.show()

def excel_chart():
    option= ['沪深300','中证500','中证800','中证1000']
    data = [[2009+i for i in range(10)]]
    for i in range(len(option)):
        df = pd.read_csv('业绩超预期{0}成分股比重（十年）.csv'.format(option[i]),names=['年份','总共超预期数量','{0}成分股数量'.format(option[i]),'比重'],encoding='utf_8_sig')
        total_num = df['总共超预期数量'].values
        name = '{0}成分股数量'.format(option[i])
        data.append(df[name].values)
    df = pd.DataFrame(data,index=['所属指数','沪深300','中证500','中证800','中证1000'])
    unique_num = []
    for i in range(2009,2019,1):
        list=[]
        for j in range(len(option)):
            df2 = pd.read_csv('业绩超预期{0}成分股（十年）.csv'.format(option[j]), names=['年份', '公告日', '代码', '名称'], encoding='utf_8_sig')
            [list.append(df2.loc[df2['年份']==i,'代码'].values[k]) for k in range(len(df2.loc[df2['年份']==i]))]
        s = pd.Series(list)
        num = s.drop_duplicates()
        unique_num.append(len(num))
    difference = total_num-unique_num
    df.loc['其他']=difference
    sum_num =[]
    length = len(df.iloc[0,:])
    for a in range(length):
        sum_num.append(sum(df.iloc[1:,a].values))
    # print(sum_num)
    df.loc['合计'] = sum_num
    # print(df)
    df.to_csv('业绩超预期指数成分股统计2009-2018.csv',index=True,header=False,encoding='utf_8_sig')

# update_zz1000_cons()

# option = ['沪深300','中证500','中证800','中证1000']
# for a in option:
    # for i in range(2009,2019,1):
    #     find_stock(i,a)

# graph()
excel_chart()