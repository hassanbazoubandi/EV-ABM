@echo off

set pre_lens=3 6 9 12
set add_feats=None
set folds=1 2 3 4 5 6
set pred_types=region
set NODE=-1
set IN_NUM_NODE=404
set OUT_NUM_NODE=404
set EPOCH=1
set feat=occ

for %%T in (%feat%) do (
    for %%l in (%pre_lens%) do (
        for %%f in (%folds%) do (
            for %%t in (%pred_types%) do (
                if %%t==node (
                    for /L %%n in (0,1,%NODE%) do (
                        python run.py ^
                          --task_name long_term_forecast ^
                          --is_training 1 ^
                          --root_path ./dataset/UrbanEV/ ^
                          --data_path occ-None.csv ^
                          --model_id st-evcdp_12_3 ^
                          --data custom ^
                          --features S ^
                          --seq_len 12 ^
                          --label_len 12 ^
                          --e_layers 1 ^
                          --factor 1 ^
                          --enc_in %IN_NUM_NODE% ^
                          --dec_in %IN_NUM_NODE% ^
                          --c_out %OUT_NUM_NODE% ^
                          --d_model 512 ^
                          --d_ff 512 ^
                          --des Exp ^
                          --batch_size 32 ^
                          --learning_rate 0.001 ^
                          --itr 1 ^
                          --train_epochs %EPOCH% ^
                          --model TimeXer ^
                          --pred_len %%l ^
                          --fold %%f ^
                          --pred_type %%n ^
                          --add_feat None ^
                          --feat %%T
                    )
                ) else (
                    for %%a in (%add_feats%) do (
                        python run.py ^
                          --task_name long_term_forecast ^
                          --is_training 1 ^
                          --root_path ./dataset/UrbanEV/ ^
                          --data_path occ-None.csv ^
                          --model_id st-evcdp_12_3 ^
                          --data custom ^
                          --features M ^
                          --seq_len 12 ^
                          --label_len 12 ^
                          --e_layers 1 ^
                          --factor 1 ^
                          --enc_in %IN_NUM_NODE% ^
                          --dec_in %IN_NUM_NODE% ^
                          --c_out %OUT_NUM_NODE% ^
                          --d_model 512 ^
                          --d_ff 512 ^
                          --des Exp ^
                          --batch_size 32 ^
                          --learning_rate 0.001 ^
                          --itr 1 ^
                          --train_epochs %EPOCH% ^
                          --model TimeXer ^
                          --pred_len %%l ^
                          --fold %%f ^
                          --pred_type %%t ^
                          --add_feat %%a ^
                          --feat %%T
                    )
                )
            )
        )
    )
)

for %%T in (%feat%) do (
    for %%l in (%pre_lens%) do (
        for %%f in (%folds%) do (
            for %%t in (%pred_types%) do (
                if %%t==node (
                    for /L %%n in (0,1,%NODE%) do (
                        python run.py ^
                          --task_name long_term_forecast ^
                          --is_training 1 ^
                          --root_path ./dataset/UrbanEV/ ^
                          --data_path occ-None.csv ^
                          --model_id traffic_12_3 ^
                          --data custom ^
                          --features S ^
                          --seq_len 12 ^
                          --label_len 12 ^
                          --e_layers 1 ^
                          --d_layers 1 ^
                          --factor 1 ^
                          --enc_in %IN_NUM_NODE% ^
                          --dec_in %IN_NUM_NODE% ^
                          --c_out %OUT_NUM_NODE% ^
                          --d_model 64 ^
                          --d_ff 64 ^
                          --top_k 1 ^
                          --des Exp ^
                          --itr 1 ^
                          --batch_size 32 ^
                          --learning_rate 0.001 ^
                          --train_epochs %EPOCH% ^
                          --model TimeNet ^
                          --pred_len %%l ^
                          --fold %%f ^
                          --pred_type %%n ^
                          --add_feat None ^
                          --feat %%T
                    )
                ) else (
                    for %%a in (%add_feats%) do (
                        python run.py ^
                          --task_name long_term_forecast ^
                          --is_training 1 ^
                          --root_path ./dataset/UrbanEV/ ^
                          --data_path occ-None.csv ^
                          --model_id traffic_12_3 ^
                          --model TimesNet ^
                          --data custom ^
                          --features M ^
                          --seq_len 12 ^
                          --label_len 12 ^
                          --e_layers 1 ^
                          --d_layers 1 ^
                          --factor 1 ^
                          --enc_in %IN_NUM_NODE% ^
                          --dec_in %IN_NUM_NODE% ^
                          --c_out %OUT_NUM_NODE% ^
                          --d_model 64 ^
                          --d_ff 64 ^
                          --top_k 1 ^
                          --des Exp ^
                          --itr 1 ^
                          --batch_size 32 ^
                          --learning_rate 0.001 ^
                          --train_epochs %EPOCH% ^
                          --pred_len %%l ^
                          --fold %%f ^
                          --pred_type %%t ^
                          --add_feat %%a ^
                          --feat %%T

                    )
                )
            )
        )
    )
)

REM 结束
echo All tasks completed!
pause
