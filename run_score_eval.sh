CUDA_VISIBLE_DEVICES=7 python pr_scoring.py --rel_set lama --model roberta-large # running
CUDA_VISIBLE_DEVICES=7 python pr_scoring.py --rel_set lama --model roberta-base --settings 5 # running
CUDA_VISIBLE_DEVICES=7 python pr_scoring.py --rel_set lama --model bert-large-cased # running 
CUDA_VISIBLE_DEVICES=7 python pr_scoring.py --rel_set lama --model distilbert-base-cased # running 
# CUDA_VISIBLE_DEVICES=7 python pr_scoring.py --rel_set lama --model bert-large-uncased

CUDA_VISIBLE_DEVICES=1 python pr_scoring.py --rel_set conceptnet --model roberta-large # need re-run
CUDA_VISIBLE_DEVICES=7 python pr_scoring.py --rel_set conceptnet --model roberta-base
CUDA_VISIBLE_DEVICES=7 python pr_scoring.py --rel_set conceptnet --model bert-large-cased
CUDA_VISIBLE_DEVICES=7 python pr_scoring.py --rel_set conceptnet --model distilbert-base-cased
# CUDA_VISIBLE_DEVICES=7 python pr_scoring.py --rel_set conceptnet --model bert-large-uncased
