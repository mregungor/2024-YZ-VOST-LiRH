#!/bin/sh
export CUDA_VISIBLE_DEVICES=1  # Set the GPU ID

python trainer.py \
    --model clip_ resnet50 --input_size 448 --reduction 8 --truncation 4 --anchor_points average --prompt_type word \
    --dataset sha --augment \
    --count_loss dmcount