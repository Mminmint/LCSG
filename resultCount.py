# -*- coding: utf-8 -*-
# @Time    : 2025/1/10 15:27
# @Author  : Mminmint
# @File    : resultCount.py
# @Software: PyCharm


import os
import xml.etree.ElementTree as ET
import pandas as pd

# 设置文件夹路径
folder_path = 'output'  # 请根据实际情况修改文件夹路径

def duration():
    # 存储结果的列表
    results = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.startswith('veh') and filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)

            # 解析XML文件
            tree = ET.parse(file_path)
            root = tree.getroot()

            # 初始化计数器和总持续时间
            count = 0
            total_duration = 0.0

            # 遍历tripinfo元素
            for tripinfo in root.findall('tripinfo'):
                arrival = float(tripinfo.get('arrival', 0))
                duration = float(tripinfo.get('duration', 0))

                # 统计arrival >= 600的车辆
                if arrival >= 600:
                    count += 1
                    total_duration += duration

                    # 计算平均duration
            average_duration = total_duration / count if count > 0 else 0

            # 将结果添加到列表中
            results.append({
                'File Name': filename,
                'Count of Vehicles (arrival >= 600)': count,
                'Average Duration': average_duration
            })

        # 创建DataFrame并写入Excel文件
    df = pd.DataFrame(results)
    output_excel_path = 'vehicle_summary.xlsx'  # 输出Excel文件名
    df.to_excel(output_excel_path, index=False)

    print(f'Results have been written to {output_excel_path}')


def emission():
    output_excel_path = 'emission_summary.xlsx'  # 输出Excel文件名

    # 存储所有文件的结果
    summary_results = []

    # 创建一个Excel writer对象
    with pd.ExcelWriter(output_excel_path) as writer:
        # 遍历文件夹中的所有文件
        for filename in os.listdir(folder_path):
            if filename.startswith('emission') and filename.endswith('.xml'):
                file_path = os.path.join(folder_path, filename)

                # 解析XML文件
                tree = ET.parse(file_path)
                root = tree.getroot()

                # 创建一个字典来存储edge数据
                edge_data = {}

                # 遍历interval中的edge元素
                for edge in root.findall('.//edge'):
                    edge_id = edge.get('id')
                    CO_perVeh = float(edge.get('CO_perVeh', 0))
                    CO2_perVeh = float(edge.get('CO2_perVeh', 0))
                    HC_perVeh = float(edge.get('HC_perVeh', 0))
                    PMx_perVeh = float(edge.get('PMx_perVeh', 0))
                    NOx_perVeh = float(edge.get('NOx_perVeh', 0))
                    fuel_perVeh = float(edge.get('fuel_perVeh', 0))

                    # 将数据存储在字典中
                    edge_data[edge_id] = {
                        'CO': CO_perVeh,
                        'CO2': CO2_perVeh,
                        'HC': HC_perVeh,
                        'PMx': PMx_perVeh,
                        'NOx': NOx_perVeh,
                        'fuel': fuel_perVeh
                    }

                    # 将字典转换为DataFrame
                df = pd.DataFrame.from_dict(edge_data, orient='index')

                # 获取文件名中的时间段信息（例如：1200veh）
                interval_info = filename.split('.')[0]  # 假设文件名格式为"1200veh.xml"

                # 将DataFrame写入Excel文件，使用interval_info作为工作表名称
                df.to_excel(writer, sheet_name=interval_info)

                # 计算每个指标的平均值并添加到summary_results
                edge_df = pd.DataFrame(edge_data).T  # 转置，使edge_id为行名
                edge_df.index.name = 'Edge ID'

                avg_values = edge_df.mean().to_dict()
                avg_values['Filename'] = filename
                summary_results.append(avg_values)

    # 创建总结表的DataFrame
    summary_df = pd.DataFrame(summary_results)
    summary_df.set_index('Filename', inplace=True)

    # 将总结表写入Excel
    with pd.ExcelWriter(output_excel_path, mode='a', engine='openpyxl') as writer:
        summary_df.to_excel(writer, sheet_name='Summary')

    print(f'Results have been written to {output_excel_path}')


if __name__ == "__main__":
    duration()
    emission()