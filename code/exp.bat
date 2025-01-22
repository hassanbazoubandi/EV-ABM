@echo off

set models=ar lo arima fcnn lstm gcn gcnlstm astgcn
set pre_lens=3 6 9 12
set folds=1 2 3 4 5 6

for %%m in (%models%) do (
    for %%l in (%pre_lens%) do (
        for %%f in (%folds%) do (
                python main.py --model %%m --pre_len %%l --fold %%f --pred_type region --add_feat None --feat occ
            )
        )
)
echo All experiments completed.
