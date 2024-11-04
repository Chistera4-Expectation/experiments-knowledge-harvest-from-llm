from utils import KnowledgeGraph, human_name, name_to_snake_case, PATH_ONTOLOGY
from relation_info import PATH as PATH_RELATION_INFO


PATH_ONTOLOGY_GPT_3_5 = PATH_ONTOLOGY / "ontology_gpt_3.5.owl"
MAX_NUMBER_SEED_ENT_TUPLES = 5
SEED = 753


if __name__ == "__main__":
    processed = set()
    json_config_file = "{\n"
    with KnowledgeGraph(PATH_ONTOLOGY_GPT_3_5) as kg:
        for cls in kg.visit_classes_depth_first():
            if human_name(cls) in processed:
                continue
            processed.add(human_name(cls))
            json_config_file += '\t"is_instance_of_{}": '.format(name_to_snake_case(human_name(cls))) + '{\n\t\t'
            json_config_file += '"init_prompts": [\n\t\t\t'
            json_config_file += '"<ENT0> is instance of {} ."\n\t\t'.format(human_name(cls))
            json_config_file += "],\n"
            # Generate the seed entity tuples (random pick from the instances of the class)
            instances = list(cls.instances())
            # Random re-arrange the instances
            instances = sorted(instances, key=lambda x: hash(x.name + str(SEED)))
            json_config_file += '\t\t"seed_ent_tuples": [\n'
            number_of_tuples = min(len(instances), MAX_NUMBER_SEED_ENT_TUPLES)
            for i in range(number_of_tuples):
                instance = instances[i]
                json_config_file += '\t\t\t[\n\t\t\t\t"{}"\n\t\t\t],\n'.format(instance.name.replace('_', ' '))
            # remove the last comma
            json_config_file = json_config_file[:-2] + "\n"
            json_config_file += "\t\t]\n"
            json_config_file += '\t},\n'
        # remove the last comma
        json_config_file = json_config_file[:-2] + "\n"
        json_config_file += '}'

    # Save the JSON configuration file
    with open(PATH_RELATION_INFO / "nutrition.json", "w") as f:
        f.write(json_config_file)
