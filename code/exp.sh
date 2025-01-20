#!/bin/bash

# Disable command echoing
set +v

models="ar lo arima fcnn lstm gcn gcnlstm astgcn"
pre_lens="3"
add_feats="None"
folds="1 2 3 4 5 6"
pred_types="region"
NODE="279"
feat="occ"

for T in $feat; do
    for m in $models; do
        for l in $pre_lens; do
            for f in $folds; do
                for a in $add_feats; do
                    python main.py --model $m --pre_len $l --fold $f --pred_type region --add_feat $a --feat $T
                done
            done
        done
    done
done

echo "All experiments completed."