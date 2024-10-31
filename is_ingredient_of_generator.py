from utils import KnowledgeGraph, human_name, name_to_snake_case, subtype
from relation_info import PATH as PATH_RELATION_INFO


if __name__ == "__main__":
    processed = set()
    json_config_file = "{\n"
    with KnowledgeGraph() as kg:
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
                json_config_file += '\t"is_ingredient_of_{}": '.format(name_to_snake_case(human_name(recipe))) + '{\n\t\t'
                json_config_file += '"init_prompts": [\n\t\t\t'
                json_config_file += '"<ENT0> is ingredient of {} ."\n\t\t'.format(human_name(recipe))
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
