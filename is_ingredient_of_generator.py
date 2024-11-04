from pathlib import Path
from utils import KnowledgeGraph, human_name, name_to_snake_case, subtype
from relation_info import PATH as PATH_RELATION_INFO
from ontologies import PATH as PATH_ONTOLOGY
import os


PATH_ONTOLOGY_POPULATED = PATH_ONTOLOGY / "populated_ontology.owl"
PATH_ONTOLOGY_FINAL = PATH_ONTOLOGY / "final_ontology.owl"
PATH_ONTOLOGY_GEMMA_2 = PATH_ONTOLOGY / "ontology_gemma_2.owl"
PATH_ONTOLOGY_GPT_3_5 = PATH_ONTOLOGY / "ontology_gpt_3.5.owl"
PATH_ONTOLOGY_GPT_4 = PATH_ONTOLOGY / "ontology_gpt_4.owl"
PATH_ONTOLOGY_LLAMA_2 = PATH_ONTOLOGY / "ontology_llama_2.owl"
PATH_ONTOLOGY_MISTRAL = PATH_ONTOLOGY / "ontology_mistral.owl"
PATH_ONTOLOGY_MIXTRAL = PATH_ONTOLOGY / "ontology_mixtral.owl"
PATH_ONTOLOGY_NOUS_HERMES = PATH_ONTOLOGY / "ontology_nous_hermes.owl"
PATH_ONTOLOGY_OPENCHAT = PATH_ONTOLOGY / "ontology_openchat.owl"
AUX_ONTOLOGIES = [PATH_ONTOLOGY_GEMMA_2, PATH_ONTOLOGY_GPT_3_5, PATH_ONTOLOGY_GPT_4, PATH_ONTOLOGY_LLAMA_2,
                  PATH_ONTOLOGY_MISTRAL, PATH_ONTOLOGY_MIXTRAL, PATH_ONTOLOGY_NOUS_HERMES, PATH_ONTOLOGY_OPENCHAT]
# AUX_ONTOLOGIES = [PATH_ONTOLOGY_GPT_3_5]
MAX_NUMBER_SEED_ENT_TUPLES = 5
SEED = 753


def populate_recipe(recipes: dict[str: list[str]], processed: set[str], ontology: Path):
    with KnowledgeGraph(ontology) as kg_aux:
        Recipe = kg_aux.onto.Recipe
        for cls in kg_aux.visit_classes_depth_first():
            if not subtype(cls, Recipe):
                continue
            # Retrieve all the recipes for the class
            instances = list(cls.instances())
            for recipe in instances:
                if human_name(recipe) in processed:
                    continue
                processed.add(human_name(recipe))
                # Get the ingredients
                ingredients = [x.name for x in getattr(recipe, kg_aux.onto.hasForIngredient.name)]
                # Add the recipe to the dictionary
                recipes[human_name(recipe)] = ingredients


if __name__ == "__main__":
    os.system("cp {} {}".format(str(PATH_ONTOLOGY_POPULATED), str(PATH_ONTOLOGY_FINAL)))
    json_config_file = "{\n"

    # Retrieve every ingredient for each recipe from the auxiliary ontology
    recipes = {}
    processed = set()
    for ontology in AUX_ONTOLOGIES:
        populate_recipe(recipes, processed, ontology)

    with KnowledgeGraph(PATH_ONTOLOGY_FINAL) as kg:
        skipped = set()
        processed = set()
        covered = set()
        processed_class = set()
        Recipe = kg.onto.Recipe
        for cls in kg.visit_classes_depth_first():
            if human_name(cls) in processed_class:
                continue
            if not subtype(cls, Recipe):
                continue
            processed_class.add(human_name(cls))
            # Retrieve all the recipes for the class
            instances = list(cls.instances())
            for recipe in instances:
                if human_name(recipe) in processed:
                    continue
                processed.add(human_name(recipe))
                tmp_json_config_file = '\t"is_ingredient_of_{}": '.format(name_to_snake_case(human_name(recipe))) + '{\n\t\t'
                tmp_json_config_file += '"init_prompts": [\n\t\t\t'
                tmp_json_config_file += '"<ENT0> is ingredient of {} ."\n\t\t'.format(human_name(recipe))
                tmp_json_config_file += "],\n"

                # Check if the recipe is present in the auxiliary ontology
                # If positive add some seed entity tuples
                if human_name(recipe) in recipes.keys() and len(recipes[human_name(recipe)]) > 0:
                    covered.add(human_name(recipe))
                    json_config_file += tmp_json_config_file
                    json_config_file += '\t\t"seed_ent_tuples": [\n'
                    number_of_tuples = min(len(recipes[human_name(recipe)]), MAX_NUMBER_SEED_ENT_TUPLES)
                    for i in range(number_of_tuples):
                        ingredient = recipes[human_name(recipe)][i]
                        json_config_file += '\t\t\t[\n\t\t\t\t"{}"\n\t\t\t],\n'.format(ingredient.replace('_', ' '))
                    # remove the last comma
                    json_config_file = json_config_file[:-2] + "\n"
                    json_config_file += "\t\t]\n"
                    json_config_file += '\t},\n'
                else:
                    skipped.add(human_name(recipe))
        # remove the last comma
        json_config_file = json_config_file[:-2] + "\n"
        json_config_file += '}'
        print("Processed recipes: {}".format(len(processed)))
        print("Covered recipes: {}".format(len(covered)))
        print("Skipped recipes: {}".format(len(skipped)))
    # Save the JSON configuration file
    with open(PATH_RELATION_INFO / "nutrition_step_2.json", "w") as f:
        f.write(json_config_file)
    os.system("rm {}".format(str(PATH_ONTOLOGY_FINAL)))
