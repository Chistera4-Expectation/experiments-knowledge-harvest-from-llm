from utils import KnowledgeGraph, human_name, name_to_snake_case, subtype
from relation_info import PATH as PATH_RELATION_INFO
from ontologies import PATH as PATH_ONTOLOGY


PATH_ONTOLOGY_POPULATED = PATH_ONTOLOGY / "populated_ontology.owl"
PATH_ONTOLOGY_AUXILIARY = PATH_ONTOLOGY / "ontology.owl"
MAX_NUMBER_SEED_ENT_TUPLES = 5
SEED = 753


if __name__ == "__main__":
    processed = set()
    json_config_file = "{\n"
    with KnowledgeGraph(PATH_ONTOLOGY_POPULATED) as kg:
        with KnowledgeGraph(PATH_ONTOLOGY_AUXILIARY) as kg_aux:
            Recipe = kg.onto.Recipe
            for cls in kg.visit_classes_depth_first():
                if human_name(cls) in processed:
                    continue
                if not subtype(cls, Recipe):
                    continue
                processed.add(human_name(cls))
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
                    cls_aux = kg_aux.onto[human_name(recipe)]
                    if cls_aux is not None:
                        instances_aux = list(cls_aux.instances())
                        if human_name(recipe) in [human_name(x) for x in instances_aux]:
                            # Retrieve ingredients
                            ingredients = [x for x in instances_aux if human_name(x) == "Ingredient"]


                    json_config_file += "],\n"
                    json_config_file += '\t\t"seed_ent_tuples": [\n'
                    json_config_file += "\t\t]\n"
                    json_config_file += '\t},\n'
            # remove the last comma
            json_config_file = json_config_file[:-2] + "\n"
            json_config_file += '}'

    # Save the JSON configuration file
    with open(PATH_RELATION_INFO / "nutrition_step_2.json", "w") as f:
        f.write(json_config_file)
