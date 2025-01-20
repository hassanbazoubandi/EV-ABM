# UrbanEV

UrbanEV is an open dataset of EV charging space availability and electricity use in Shenzhen, China.

<!-- >Qu, H., Kuang, H., Li, J., & You, L. (2023). A physics-informed and attention-based graph learning approach for regional electric vehicle charging demand prediction. IEEE Transactions on Intellgent Transportation Systems. [Paper in IEEE Explore](https://ieeexplore.ieee.org/document/10539613) [Paper in arXiv](https://arxiv.org/abs/2309.05259) -->

<!-- ```shell

``` -->

Author: Haohao Qu (haohao.qu@connect.polyu.hk)

## Updates

* January 19, 2025: Upload code and data for distribution prediction based on UrbanEV .

## Data Description

The raw dataset compiles comprehensive information on **1,682** public charging stations and **24,798** public charging piles, covering a time period from **1 September 2022 to 28 February 2023 with hourly granularity**, enabling the exploration of short-, mid-, and long-term forecasting scenarios. Specifically, it provides three types of charging data (occupancy, duration, and volume), four dynamic factors (electricity price, service price, weather conditions, and time of day), three spatial attributes (adjacency, distance, and coordinates), and four static coefficients (point of interest, area, pile number, and station number). You can download the raw data from [Google Drive Link](https://drive.google.com/drive/folders/1VUgdb8uNgmtvO93BHBK_OrSxjndrF-48?usp=sharing).

 After applying various data processing techniques, the dataset is refined to **1,362** charging stations and **17,532** charging piles, making it well-suited for charging demand prediction. Additionally, the data is organized into traffic zones, offering a new perspective on regional EV charging patterns. You can find the zone-level data in `./data/dataset/`

![avatar](figs/map.png) Figure 1. Spatial distribution of 1,682 public charging stations and 24,798 charging piles in the UrbanEV dataset.

## Files

**code**：传统模型以及深度模型进行基于UrbanEV数据集的Distribution时序预测的相关代码以及提供部分模块化功能

* `baselines.py`: three traditional forecasting methods，i.e. the last observation (LO), Auto-regressive (AR), and Auto-regressive Integrated Moving Average(ARIMA) model. 以及The six deep learning models代码，i.e. fully connected neural network (FCNN), Long Short-Term Memory (LSTM), Graph Convolutional Network (GCN), GCN-LSTM, Attention-Based Spatial-Temporal Graph Convolutional Network (ASTGCN)
* `exp.bat`|`exp.sh`: Distribution时序预测的脚本文件
* `init_env.bat`|`init_env.sh`: 创建能运行基于UrbanEV数据集的时序预测的虚拟环境
* `main.py`: 主函数文件
* `parse.py`: 这个文件提供了一个命令行接口，用于配置时空电动车充电需求预测模型的训练参数。
* `preprocess.py`: 将`./data/dataset`文件夹下的数据转换成基于Transformer的时序模型能够训练并预测的数据
* `train.py`: 模型训练文件
* `utils.py`: 与Urban数据集预测相关的封装好的功能，e.g. 时序交叉验证数据划分、时序数据集准备

**data**: zone-level的Urban数据集，经过异常值检测、0值判断等等，最后总共包括275个区域，1362个充电站，17532个充电桩。

* `adj.csv`: 邻接矩阵
* `duration.csv`: Hourly EV charging duration (Unit: hour).
* `e_price.csv`: Electricity price (Unit: Yuan/kWh).
* `inf.csv`: Important information of the 1362 charging stations, including coordinates and charging capacities.
* `occupancy.csv`: Hourly EV charging occupancy  rate (Unit: %).
* `s_price.csv`: Service price (Unit: Yuan/kWh).
* `volume.csv`: Hourly EV charging volume (Unit: kWh).
* `weather_airport.csv`: 归一化后的Weather data collected from the meteorological station at Bao'an Airport (Shenzhen) ，.
* `weather_central.csv`: 归一化后的Weather data collected from Futian Meteorological Station located in the city centre area of Shenzhen.
* `weather_header.csv`: Descriptions of the table headers presented in `weather_airport.csv` and `weather_central.csv`.
* `zone_dist.csv`: 275个区域之间的距离矩阵

**code_transformer**:基于Transformer结构模型进行基于UrbanEV数据集的Distribution时序预测的相关代码，以下是部分与基于UranEV数据集预测相关的核心文件及文件夹的解释：

* `dataset/st-evcdp` 该目录下存放预测用到的数据文件，数据文件可以通过`../code/preprocess.py`生成
* `exp.bat`|`exp.sh`: 用于基于Transformer的模型进行Distribution时序预测的脚本文件

## Enviroment Requirement

该部分为基于UrbanEV的时序预测所需虚拟环境的搭建，使用的python版本为3.8，torch版本为2.4.1.  假设你的路径是项目的根目录

以下是相关的执行命令:

### Windows

```shell
cd code
./init_env.bat
```

### Linux

```shell
cd code
./init_env.sh
```

由于PyG Temporal 目前停止维护，因此在运行`ASTGCN`时序预测实验中会出现ModuleNotFoundError: No module named 'torch_geometric.utils.to_dense_adj'。需要将`from torch_geometric.utils.to_dense_adj import to_dense_adj` 改为 `from torch_geometric.utils import to_dense_adj`,见[pyg-#9023 (reply in thread)](https://github.com/pyg-team/pytorch_geometric/discussions/9023#discussioncomment-8813817)

## Run Distribution Prediction on the UrbanEV dataset

假设你的路径是项目的根目录

### Simple Example

**Traditional and deep learning-based model**

```shell
cd code
conda activate UrbanEV
python main.py --model=fcnn --pre_len=3 --fold=1 --pred_type=region --add_feat=None --feat occ --epoch 1
```

**Traansformer-based model**

```shell
cd code-transformer
conda activate UrbanEV
python run.py --task_name long_term_forecast --is_training 1 --root_path ./dataset/UrbanEV/ --data_path occ-e.csv --model_id st-evcdp_12_3 --model TimeXer --data custom --features M --seq_len 12 --label_len 12 --e_layers 1 --factor 1 --enc_in 608 --dec_in 608 --c_out 304 --d_model 512 --d_ff 512 --des Exp --batch_size 32 --learning_rate 0.001 --itr 1 --train_epochs 1 --pred_len 3 --pred_type region --add_feat None --fold 3 --feat occ
```

### Distribution Prediction for Tradditional and Deep Learning Model

**Windows**

```shell
cd code
conda activate UrbanEV
./exp.bat
```

**Linux**

```shell
cd code
conda activate UrbanEV
./exp.sh
```

### Distribution Prediction for Transformer-based Model

**Windows**

```shell
cd code
conda activate UrbanEV
python preprocess.py
cd ..
cd code-transformer
./exp.bat
```

**Linux**

```shell
cd code
conda activate UrbanEV
python preprocess.py
cd ..
cd code-transformer
./exp.sh
```

More updates will be posed in the near future! Thank you for your interest.
