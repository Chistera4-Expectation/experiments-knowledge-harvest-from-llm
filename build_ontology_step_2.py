from utils import KnowledgeGraph, human_name, subtype, get_filtered_instances
from ontologies import PATH as PATH_ONTOLOGY
from results import PATH as PATH_RESULTS
import fire
import json
import os


THRESHOLD = 0.00001


def main(rel_set='nutrition_step_2',
         model_name='roberta-large',
         max_n_ent_tuples=10000,
         max_n_prompts=20,
         use_init_prompts=False):
    path_results = PATH_RESULTS / rel_set / f"{max_n_ent_tuples}tuples_top{max_n_prompts}prompts" / model_name
    if use_init_prompts:
        path_results = PATH_RESULTS / rel_set / f"{max_n_ent_tuples}tuples_initprompts" / model_name
    path_populated_ontology = PATH_ONTOLOGY / f"{model_name}_populated.owl"
    path_final_ontology = PATH_ONTOLOGY / f"{model_name}_populated_final.owl"
    processed_classes = set()
    processed_recipes = set()
    results_file = path_results / "is_ingredient_of" / "ent_tuples.json"
    recipes: dict[str: list[str]] = {}
    with open(results_file, "r") as f:
        results = json.load(f)
    for result in results:
        # Add the ingredient to the list of ingredients for the recipe
        # Only if the confidence is above the threshold
        if result[1] > THRESHOLD:
            ent0, ent1 = result[0]
            if ent1 not in recipes:
                recipes[ent1] = []
            recipes[ent1].append(ent0)
    os.system("cp {} {}".format(str(path_populated_ontology), str(path_final_ontology)))
    with KnowledgeGraph(path_final_ontology) as kg:
        Recipe = kg.onto.Recipe
        for cls in kg.visit_classes_depth_first():
            if not subtype(cls, Recipe):
                continue
            if human_name(cls) in processed_classes:
                continue
            processed_classes.add(human_name(cls))
            # Retrieve all the recipes for the class
            instances = list(get_filtered_instances(cls, path_final_ontology.name[:-4]))
            for recipe in instances:
                if human_name(recipe) in recipes.keys() and len(recipes[human_name(recipe)]) > 0:
                    processed_recipes.add(human_name(recipe))
                    print("Processed: {}".format(human_name(recipe)))
                    # Add the ingredients to the recipe
                    for ingredient in recipes[human_name(recipe)]:
                        if kg.onto[ingredient] is not None:
                            print("Ingredient: {}".format(ingredient))
                            ingredient = kg.onto[ingredient]
                            kg.add_property(recipe, kg.onto.hasForIngredient, ingredient)
                            kg.add_property(ingredient, kg.onto.ingredientOf, recipe)

        # Save the populated ontology
        print("Processed {} recipes".format(len(processed_recipes)))
        kg.save()


if __name__ == "__main__":
    fire.Fire(main)
