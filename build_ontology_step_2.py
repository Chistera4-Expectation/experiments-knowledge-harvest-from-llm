from utils import KnowledgeGraph, human_name, name_to_snake_case, subtype, get_filtered_instances
from ontologies import PATH as PATH_ONTOLOGY
from results import PATH as PATH_RESULTS
import json
import os


PATH_RESULTS = PATH_RESULTS / "nutrition_step_2" / "10000tuples_top20prompts" / "roberta-large"
PATH_POPULATED_ONTOLOGY = PATH_ONTOLOGY / "populated_ontology.owl"
PATH_FINAL_ONTOLOGY = PATH_ONTOLOGY / "final_ontology.owl"
THRESHOLD = 0.00001


if __name__ == "__main__":
    processed_classes = set()
    processed_recipes = set()
    results_file = PATH_RESULTS / "is_ingredient_of" / "ent_tuples.json"
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
    os.system("cp {} {}".format(str(PATH_POPULATED_ONTOLOGY), str(PATH_FINAL_ONTOLOGY)))
    with KnowledgeGraph(PATH_FINAL_ONTOLOGY) as kg:
        Recipe = kg.onto.Recipe
        for cls in kg.visit_classes_depth_first():
            if not subtype(cls, Recipe):
                continue
            if human_name(cls) in processed_classes:
                continue
            processed_classes.add(human_name(cls))
            # Retrieve all the recipes for the class
            instances = list(get_filtered_instances(cls, PATH_FINAL_ONTOLOGY.name[:-4]))
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
