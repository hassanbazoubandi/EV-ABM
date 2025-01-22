#!/bin/bash

pre_lens=(3 6 9 12)
folds=(1 2 3 4 5 6)
IN_NUM_NODE=404
OUT_NUM_NODE=404
EPOCH=1

for l in "${pre_lens[@]}"; do
    for f in "${folds[@]}"; do
        python run.py \
            --task_name long_term_forecast \
            --is_training 1 \
            --root_path ./dataset/UrbanEV/ \
            --data_path occ-None.csv \
            --data custom \
            --features M \
            --seq_len 12 \
            --label_len 12 \
            --e_layers 1 \
            --factor 1 \
            --enc_in $IN_NUM_NODE \
            --dec_in $IN_NUM_NODE \
            --c_out $OUT_NUM_NODE \
            --d_model 512 \
            --d_ff 512 \
            --des Exp \
            --batch_size 32 \
            --learning_rate 0.001 \
            --itr 1 \
            --train_epochs $EPOCH \
            --model TimeXer \
            --pred_len $l \
            --fold $f \
            --pred_type region \
            --add_feat None \
            --feat occ
    done
done

for l in "${pre_lens[@]}"; do
    for f in "${folds[@]}"; do
        python run.py \
            --task_name long_term_forecast \
            --is_training 1 \
            --root_path ./dataset/UrbanEV/ \
            --data_path occ-None.csv \
            --data custom \
            --features M \
            --seq_len 12 \
            --label_len 12 \
            --e_layers 1 \
            --d_layers 1 \
            --factor 1 \
            --enc_in $IN_NUM_NODE \
            --dec_in $IN_NUM_NODE \
            --c_out $OUT_NUM_NODE \
            --d_model 64 \
            --d_ff 64 \
            --top_k 1 \
            --des Exp \
            --itr 1 \
            --batch_size 32 \
            --learning_rate 0.001 \
            --train_epochs $EPOCH \
            --model TimesNet \
            --pred_len $l \
            --fold $f \
            --pred_type region \
            --add_feat None \
            --feat occ
    done
done

echo "All tasks completed!"
