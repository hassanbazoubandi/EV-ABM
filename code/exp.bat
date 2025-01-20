@echo off

set models=ar lo arima fcnn lstm gcn gcnlstm astgcn
set pre_lens=3
set add_feats=None
set folds=1 2 3 4 5 6
set pred_types=region
set NODE=279
set feat=occ


for %%T in (%feat%) do (
    for %%m in (%models%) do (
        for %%l in (%pre_lens%) do (
            for %%f in (%folds%) do (
                for %%a in (%add_feats%) do (
                    python main.py --model %%m --pre_len %%l --fold %%f --pred_type region --add_feat %%a --feat %%T
                )
            )
        )
    )
)
echo All experiments completed.
