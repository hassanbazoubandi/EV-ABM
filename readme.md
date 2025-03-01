# UrbanEV

UrbanEV is an open dataset of EV charging space availability and electricity use in Shenzhen, China. This project is dedicated to the public domain using the [CC0 1.0 Universal License](LICENSE). For more information, see [Creative Commons - CC0](https://creativecommons.org/publicdomain/zero/1.0/).

<!-- >Qu, H., Kuang, H., Li, J., & You, L. (2023). A physics-informed and attention-based graph learning approach for regional electric vehicle charging demand prediction. IEEE Transactions on Intellgent Transportation Systems. [Paper in IEEE Explore](https://ieeexplore.ieee.org/document/10539613) [Paper in arXiv](https://arxiv.org/abs/2309.05259) -->

<!-- ```shell

``` -->

## Contact

If you have any questions regarding this dataset, feel free to reach out.

Author: Han Li (lihan76@mail2.sysu.edu.cn), Haohao Qu (haohao.qu@connect.polyu.hk)

## Updates

* January 19, 2025: Upload code and data for distribution prediction based on UrbanEV .

## Data Description

The raw dataset compiles comprehensive information on **1,682** public charging stations and **24,798** public charging piles, covering a time period from **1 September 2022 to 28 February 2023 with hourly granularity**, enabling the exploration of short-, mid-, and long-term forecasting scenarios. Specifically, it provides three types of charging data (occupancy, duration, and volume), four dynamic factors (electricity price, service price, weather conditions, and time of day), three spatial attributes (adjacency, distance, and coordinates), and four static coefficients (point of interest, area, pile number, and station number). You can download the raw data from [Google Drive Link](https://drive.google.com/drive/folders/1VUgdb8uNgmtvO93BHBK_OrSxjndrF-48?usp=sharing).

 After applying various data processing techniques, the dataset is refined to **1,362** charging stations and **17,532** charging piles, making it well-suited for charging demand prediction. Additionally, the data is organized into traffic zones, offering a new perspective on regional EV charging patterns. You can find the zone-level data in `./data/dataset/`

![avatar](figs/map.png) Figure 1. Spatial distribution of 1,682 public charging stations and 24,798 charging piles in the UrbanEV dataset.

## Files

**code**: Code for distribution time-series prediction using traditional models and deep learning models based on the UrbanEV dataset, including several modularized functions.

* `baselines.py`: Includes three traditional forecasting methods (Last Observation, Auto-regressive (AR), and ARIMA) and six deep learning models (Fully Connected Neural Network (FCNN), Long Short-Term Memory (LSTM), Graph Convolutional Network (GCN), GCN-LSTM, Attention-Based Spatial-Temporal Graph Convolutional Network (ASTGCN)).
* `exp.bat`|`exp.sh`: Scripts for distribution time-series prediction.
* `init_env.bat`|`init_env.sh`: Scripts to create a virtual environment for running time-series predictions based on the UrbanEV dataset.
* `main.py`: Main script file.
* `parse.py`: Provides a command-line interface to configure training parameters for spatiotemporal EV charging demand prediction models.
* `preprocess.py`: Converts data in the `./data/dataset` folder into a format suitable for training and predicting with Transformer-based time-series models.
* `train.py`: Model training script.
* `utils.py`: Utility functions related to the UrbanEV dataset predictions, e.g., time-series cross-validation and dataset preparation.

**data**:  5-minute and 1-hour resolution region-level data of the UrbanEV dataset, which has been cleaned through outlier detection, zero-value checks, etc., and includes data from **275 zones**, **1,362 charging stations**, and **17,532 charging piles**.

* `5-minutes.zip`: To facilitate more detailed predictive analyses, the 5-minute resolution region-level datasets are made available, providing comprehensive access to time-series data at multiple granularities.
* `adj.csv`: Adjacency matrix.
* `duration.csv`: Hourly EV charging duration (Unit: hour).
* `e_price.csv`: Electricity price (Unit: Yuan/kWh).
* `inf.csv`: Key information about the 275 zones, including coordinates, charging capacities, area (Unit: m^2), and perimeter (Unit: m).
* `occupancy.csv`: Hourly EV charging occupancy rate (Unit: %).
* `s_price.csv`: Service price (Unit: Yuan/kWh).
* `volume.csv`: Hourly EV charging volume (Unit: kWh). The volume in \emph{volume.csv} is derived from the rated power of charging piles
* `volume-11kW.csv` provides an alternative vehicle-side estimation of charging volume to mitigate potential overestimation in `volume.csv`. Specifically, for direct current charging stations, the volume is calculated using the standard power of the most commonly used electric vehicle, Tesla Model Y (11kW), instead of the rated power of the charging pile.
* `weather_airport.csv`: Weather data from the meteorological station at Bao'an Airport (Shenzhen). These are the raw data collected, and it is recommended to use the **Max-Min** method for normalization.
* `weather_central.csv`: Weather data from Futian Meteorological Station in the city center of Shenzhen.
* `weather_header.txt`: Descriptions of the table headers in `weather_airport.csv` and `weather_central.csv`.
* `distance.csv`: Distance matrix between the 275 zones.
* `poi.csv`: Points of Interest categorized into three types: `food and beverage services`, `business and residential`, and `lifestyle services`. The coordinates used are based on the `WGS84` coordinate system.

**code_transformer**: Code for distribution time-series prediction using Transformer-based models on the UrbanEV dataset. Below are explanations for some core files and directories related to UrbanEV prediction:

* `dataset/st-evcdp`: Contains data files used for predictions, which can be generated through `../code/preprocess.py`.
* `exp.bat`|`exp.sh`: Scripts for distribution time-series prediction using Transformer-based models.


## Environment Requirements

This section outlines the setup for the virtual environment required for time-series prediction based on UrbanEV, using Python 3.8 and PyTorch 2.4.1. Assuming your working directory is the project root directory, here are the relevant commands:

### Windows

```shell
cd code
init_env.bat
```

### Linux

```shell
cd code
./init_env.sh
```

Due to the discontinuation of PyG Temporal, you may encounter a ModuleNotFoundError: No module named 'torch_geometric.utils.to_dense_adj' when running ASTGCN experiments. To resolve this, change from torch_geometric.utils.to_dense_adj import to_dense_adj to from torch_geometric.utils import to_dense_adj. See[pyg-#9023 (reply in thread)](https://github.com/pyg-team/pytorch_geometric/discussions/9023#discussioncomment-8813817) for more details.

## Run Distribution Prediction on the UrbanEV dataset

Assuming your working directory is the project root directory

### Simple Example

**Traditional and deep learning-based model**

```shell
cd code
conda activate UrbanEV
python main.py --model=fcnn --pre_len=3 --fold=1 --pred_type=region --add_feat=None --feat occ --epoch 1
```

**Transformer-based model**

```shell
cd code-transformer
conda activate UrbanEV
python run.py --task_name long_term_forecast --is_training 1 --root_path ./dataset/UrbanEV/ --data_path occ-e.csv --model_id st-evcdp_12_3 --model TimeXer --data custom --features M --seq_len 12 --label_len 12 --e_layers 1 --factor 1 --enc_in 608 --dec_in 608 --c_out 304 --d_model 512 --d_ff 512 --des Exp --batch_size 32 --learning_rate 0.001 --itr 1 --train_epochs 1 --pred_len 3 --pred_type region --add_feat None --fold 3 --feat occ
```

### Tradditional and Deep Learning Model

**Windows**

```shell
cd code
conda activate UrbanEV
exp.bat
```

**Linux**

```shell
cd code
conda activate UrbanEV
./exp.sh
```

### Transformer-based Model

**Windows**

```shell
cd code
conda activate UrbanEV
python preprocess.py
cd ..
cd code-transformer
exp.bat
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

## Acknowledgement

The project is based on the following time series forecasting repositories, from which you can explore more about the models and methods by clicking on the respective links:

* Time Series Library (TSLib)：[https://github.com/thuml/Time-Series-Library](https://github.com/thuml/Time-Series-Library).
* PyG Temporal: [https://github.com/benedekrozemberczki/pytorch_geometric_temporal](https://github.com/benedekrozemberczki/pytorch_geometric_temporal)



More updates will be posed in the near future! Thank you for your interest.
