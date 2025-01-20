#!/bin/bash

# Disable command echoing
set +v

pre_lens="3 6 9 12"
add_feats="None"
folds="1 2 3 4 5 6"
pred_types="region"
NODE=-1
IN_NUM_NODE=404
OUT_NUM_NODE=404
EPOCH=1
feat="occ"

run_model() {
    python run.py \
      --task_name long_term_forecast \
      --is_training 0 \
      --root_path ./dataset/st-evcdp/ \
      --data_path st-evcdp.csv \
      --model_id "$4" \
      --data custom \
      --features "$5" \
      --seq_len 12 \
      --label_len 12 \
      --e_layers 1 \
      --factor 1 \
      --enc_in $IN_NUM_NODE \
      --dec_in $IN_NUM_NODE \
      --c_out $OUT_NUM_NODE \
      --d_model $6 \
      --d_ff $6 \
      --des Exp \
      --batch_size 32 \
      --learning_rate 0.001 \
      --itr 1 \
      --train_epochs $EPOCH \
      --model "$7" \
      --pred_len "$2" \
      --fold "$3" \
      --pred_type "$8" \
      --add_feat "$9" \
      --feat "$1"
}

for T in $feat; do
    for l in $pre_lens; do
        for f in $folds; do
            for t in $pred_types; do
                if [ "$t" == "node" ]; then
                    for ((n=0; n<=$NODE; n++)); do
                        run_model "$T" "$l" "$f" "st-evcdp_12_3" "S" 512 "TimeXer" "$n" "None"
                    done
                else
                    for a in $add_feats; do
                        run_model "$T" "$l" "$f" "st-evcdp_12_3" "M" 512 "TimeXer" "$t" "$a"
                    done
                fi
            done
        done
    done
done

for T in $feat; do
    for l in $pre_lens; do
        for f in $folds; do
            for t in $pred_types; do
                if [ "$t" == "node" ]; then
                    for ((n=0; n<=$NODE; n++)); do
                        run_model "$T" "$l" "$f" "traffic_12_3" "S" 64 "TimeNet" "$n" "None"
                    done
                else
                    for a in $add_feats; do
                        run_model "$T" "$l" "$f" "traffic_12_3" "M" 64 "TimesNet" "$t" "$a"
                    done
                fi
            done
        done
    done
done

echo "All tasks completed!"

# Prevent the script from closing immediately (pause equivalent)
read -p "Press [Enter] key to continue..."