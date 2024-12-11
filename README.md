# Additional experiments for the paper "Large language models as oracles for instantiating ontologies with domain-specific knowledge"

## Using BertNet: Harvesting Knowledge Graphs from PLMs

This is a fork (of a fork) of the original [repository](https://github.com/tanyuqian/knowledge-harvest-from-lms) that contains the code of the following paper:

**[BertNet: Harvesting Knowledge Graphs from Pretrained Language Models](https://arxiv.org/pdf/2206.14268.pdf)** \
Shibo Hao*, Bowen Tan*, Kaiwen Tang*, Hengzhe Zhang, Eric P. Xing, Zhiting Hu \
(* Equal contribution)

## Our experiments
To adapt the work of the original repository to our experiments in order to populate an ontology we perform two main steps:
1. Generate individuals for the classes of the ontology

   1.1. we created the `nutrition_step_1.json` relation set (in the `relation_info` folder) -- one relation for each class, one placeholder for the individual -- that is needed to generate the individuals
   
   1.2. we generate individuals for the classes of the nutrition ontology

   1.3 we create the populated ontology with the individuals generated

2. Generate relations between the individuals in the recipe subclasses of the ontology

   2.1. we created the `nutrition_step_2.json` relation set (in the `relation_info` folder) -- one relation only with two placeholders, one for the recipe and one for the ingredient -- that is needed to generate the relations

   2.2 we generate relations between the individuals in the recipe subclasses of the ontology

   2.3 we create the populated ontology with the individuals and relations generated

## How to run
To run our experiments, you should configure your environment as described in the original repository.
Then, you can run the following commands:

### Step 1

```
python main.py --rel_set nutrition_step_1 --model_name roberta-large --n_ent_tuples 100 --n_prompts 20
```

This command generate the individuals of the classes of the nutrition ontology.
In our experiments, we used the following hyperparameters:
* `--rel_set`: the set of relations, must be `nutrition_step_1` for this step.
* `--model_name`: we used `roberta-large`, `roberta-base` and `bert-large-cased`.
* `--n_ent_tuples`: the number of individuals to be generated for each class (we used 100).
* `--n_prompts`: the number of prompts to be used in the search of individuals (we used 20).

```
python build_ontology_step_1.py --rel_set nutrition_step_1 --model_name roberta-large --n_ent_tuples 100 --n_prompts 20 --threshold 0.001
```

This command generates the relations of the nutrition ontology with the individuals generated in the previous step.
In our experiments, we used the following hyperparameters: 
* `--rel_set`: the set of relations, must be `nutrition_step_1` for this step.
* `--model_name`: we used `roberta-large`, `roberta-base` and `bert-large-cased`.
* `--n_ent_tuples`: the number of individuals to be generated for each class (we used 100).
* `--n_prompts`: the number of prompts to be used in the search of individuals (we used 20).
* `--threshold`: the threshold to filter the relations (we used 0.001 for `roberta-large` and `roberta-based`, 0.0001 for `bert-large-cased`).

The threshold parameter is used to filter the individuals that are unlikely to be relevant to the ontology.
The chosen threshold values were a good trade-off between the number of individuals generated and the quality of the generated individuals.

### Step 2

```
python main.py --rel_set nutrition_step_2 --model_name roberta-large --n_ent_tuples 10000 --n_prompts 20
```

This command generates the relations between the individuals in the recipe subclasses of the nutrition ontology.
In our experiments, we used the following hyperparameters:
* `--rel_set`: the set of relations, must be `nutrition_step_2` for this step.
* `--model_name`: we used `roberta-large`, `roberta-base` and `bert-large-cased`.
* `--n_ent_tuples`: the number of relations to be generated (we used 10000).
* `--n_prompts`: the number of prompts to be used in the search of relations (we used 20).

```
python build_ontology_step_2.py --rel_set nutrition_step_2 --model_name roberta-large --n_ent_tuples 10000 --n_prompts 20 --threshold 0.00001
```

This command generates the relations between the individuals in the recipe subclasses of the nutrition ontology.
In our experiments, we used the following hyperparameters:
* `--rel_set`: the set of relations, must be `nutrition_step_2` for this step.
* `--model_name`: we used `roberta-large`, `roberta-base` and `bert-large-cased`.
* `--n_ent_tuples`: the number of relations to be generated (we used 10000).
* `--n_prompts`: the number of prompts to be used in the search of relations (we used 20).
* `--threshold`: the threshold to filter the relations (we used 0.00001).

The relations `has_ingredient_of` are actually included into the ontology if both the recipe and the ingredient are present in the ontology. 


## Results
The output of the `main.py` commands are saved in the `results/` folder (see the `results/nutrition_step_1/*` and `results/nutrition_step_2/*` folders).
`build_ontology_step_2.py` creates the final ontology in the `ontologies/` folder:
* `ontologies/roberta-large_populated_final.owl`
* `ontologies/roberta-base_populated_final.owl`
* `ontologies/bert-large-cased_populated_final.owl`

## Requirements
We use `python 3.10` and all the required packages can be installed by pip:
```
pip install -r requirements.txt
```

## Harvesting KGs from LMs
For all other details, please refer to the original repository.