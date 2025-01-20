@echo off
REM Create and activate a conda environment named UrbanEV
call conda create -n UrbanEV python=3.8 --yes
call conda activate UrbanEV

REM Install PyTorch and its dependencies
pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu118

REM Install torch_geometric-temporal
pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.4.0+cu118.html
pip install torch_geometric
pip install torch-geometric-temporal

pip install statsmodels
pip install scikit-learn
pip install openpyxl
pip install patool
pip install sktime
pip install matplotlib
pip install reformer_pytorch

echo Setup completed for UrbanEV environment.
pause