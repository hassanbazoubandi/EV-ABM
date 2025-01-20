import pandas as pd
import numpy as np
from utils import read_data
from parse import parse_args
import  os

NODE = 275
args = parse_args()
# 定义附加特征类型
addition_features = ['None','T', 'P0','U', 'e', 's', 'P0+s', 'T+e', 'U+T', 's+e', 'all']
pred_types = ['region']
feat_args = ['occ']
output_dir = '../code-transformer/dataset/UrbanEV'
os.makedirs(output_dir,exist_ok=True)
for feat_arg in feat_args:
    args.feat = feat_arg
    for addition_feature in addition_features:
        args.add_feat = addition_feature
        for pred_type in pred_types:
            args.pred_type = pred_type
            feat, adj, extra_feat, time = read_data(args)
            if pred_type == 'node':
                for node_idx in range(NODE):
                    data = feat[:,node_idx]
                        
                    # 转换为 DataFrame
                    data = pd.DataFrame(data)

                    # 生成列名，确保为字符串类型
                    columns = ['OT']
                    data.columns = columns

                    # 插入日期列
                    data.insert(0, 'date', time)

                    output_path = os.path.join(output_dir,f'{args.feat}-{addition_feature}_node-{node_idx}.csv')
                    # 保存为 CSV 文件
                    data.to_csv(output_path, index=False, header=True)
            else:
                data = feat
                if addition_feature != 'None':
                    extra_feat = extra_feat.reshape(extra_feat.shape[0], -1)
                    data = np.concatenate((feat, extra_feat), axis=1)
                
                # 转换为 DataFrame
                data = pd.DataFrame(data)

                # 生成列名，确保为字符串类型
                columns = ['OT'] + [str(i) for i in range(1,data.shape[1])]
                data.columns = columns

                # 插入日期列
                data.insert(0, 'date', time)

                output_path = os.path.join(output_dir, f'{args.feat}-{addition_feature}.csv')
                # 保存为 CSV 文件
                data.to_csv(output_path, index=False, header=True)
print("process over.")


