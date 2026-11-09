'''
Replaces the gendered tokens with their neutral equivalent.

Usage
-----
FULL SWAP INCORRECT FILTERED
python3 rule-based-model/scripts/gender_neutralisation.py rule-based-model/data/gendered_tokens/noun_dependents_incorrect_filtered.json rule-based-model/data/UD_Valico/it_valico-ud-test.conllu manual_valicə_filt_full_swap

FULL SWAP CORRECT FILTERED
python3 rule-based-model/scripts/gender_neutralisation.py rule-based-model/data/gendered_tokens/noun_dependents_correct_filtered.json rule-based-model/data/UD_Valico/not-to-release/corrected/it_thvalico-ud-test.conllu manual_valicə_corr_filt_full_swap

FULL SWAP INCORRECT UNFILTERED
python3 rule-based-model/scripts/gender_neutralisation.py rule-based-model/data/gendered_tokens/noun_dependents_incorrect.json rule-based-model/data/UD_Valico/it_valico-ud-test.conllu manual_valicə_nonfilt_full_swap

FULL SWAP CORRECT UNFILTERED
python3 rule-based-model/scripts/gender_neutralisation.py rule-based-model/data/gendered_tokens/noun_dependents_correct.json rule-based-model/data/UD_Valico/not-to-release/corrected/it_thvalico-ud-test.conllu manual_valicə_corr_nonfilt_full_swap

Optional - add divide
This is so as to only neutralise part of the dataset.
---------------------
PARTIAL 1 ONE-WAY SWAP
python3 rule-based-model/scripts/gender_neutralisation.py rule-based-model/data/gendered_tokens/noun_dependents_incorrect_filtered.json rule-based-model/data/UD_Valico/it_valico-ud-test.conllu manual_valicə_filt_partial_swap_1 --divide partial1

PARTIAL 2 ONE-WAY SWAP
python3 rule-based-model/scripts/gender_neutralisation.py rule-based-model/data/gendered_tokens/noun_dependents_incorrect_filtered.json rule-based-model/data/UD_Valico/it_valico-ud-test.conllu manual_valicə_filt_partial_swap_2 --divide partial2

'''

import argparse
import json
from conllu import parse_incr
from tqdm import tqdm

def load_replacements(file_name):
    """
    Loads and clean the tsv file.
    Necessary because some entries have an unnecessary 3rd element (space). 
    """

    with open(file_name, "r", encoding="utf-8") as f:

        replacements = f.readlines()

    replacements = [line.strip().split("\t") for line in replacements]

    return replacements

def load_gendered_words(input_file):
    """
    Loads a json file containing gendered words.
    Can be either correct/incorrect, filtered/unfiltered
    """

    with open(input_file, "r") as file:

        gendered_words = json.load(file)

    return gendered_words

def align_uppercase(form, neu_form):
    """
    Ensures the capitalisation is the same in the original Valico, as certain words are uppercase.
    """
    if form.isupper():
        return neu_form.upper()
    elif form[0].isupper():
        return neu_form.capitalize()
    return neu_form

def find_replacement(gendered_words, replacements):
    '''
    Loops over the list of gendered words, find their replacement in the replacements.tsv
    If no replacement is found in the list, then it instead use the rule-based approach
    '''

    gn_forms = [x[0] for x in replacements]
    neu_forms = [x[1] for x in replacements]

    res = []

    for entry in gendered_words:

        sent_id = entry["sent_id"]

        neutralized_entry = {}

        for token in entry["instances"]:

            form = token["form"]
            id = token["id"]
            dependents = token["dependents"]

            for gn_form, neu_form in replacements:
                    if form.lower() == gn_form:

                        neutralized_entry["sent_id"] = sent_id
                        neutralized_entry["form"] = form
                        neutralized_entry["neutralized_form"] = align_uppercase(form, neu_form)
                        neutralized_entry["token_id"] = id

                        neutralized_entry["neutralized_dependents"] = []

                        for dependent in dependents:
                                                        
                            dependent_form = dependent["form"]
                            dependent_id = dependent["id"]
                            dependent_number = dependent["number"]

                            dependent_entry = {}

                            dependent_entry["form"] = dependent_form
                            dependent_entry["dependent_id"] = dependent_id

                            if dependent_form.lower() in gn_forms:

                                for gn_form, neu_form in replacements:

                                    if dependent_form.lower() == gn_form:

                                        dependent_entry["neutralized_form"] = align_uppercase(form, neu_form) 

                                        neutralized_entry["neutralized_dependents"].append(dependent_entry)
                                
                            else:

                                last_letter = dependent_form[-1]
                                vowels = 'aeiou'

                                if dependent_number == "Sing" and last_letter in vowels:
                                    dependent_entry["neutralized_form"] = dependent_form[:-1] + "ə"

                                elif dependent_number == "Plur" and last_letter in vowels:
                                    dependent_entry["neutralized_form"] = dependent_form[:-1] + "ɜ"
                                
                                else:
                                    dependent_entry["neutralized_form"] = dependent_form

                                neutralized_entry["neutralized_dependents"].append(dependent_entry)
                        res.append(neutralized_entry)
    return res

def get_unique_occurences(res):
    '''
    Gets all the unique occurences of a sentence in the gender neutralises data.
    If a sentence is unique, it means that it only contains 1 human aniamte and its dependents.
    If not, it contains two or more, which means we can divide the data in multiple ways.
    '''
    counter = {}

    for element in res:
        sent_id = element["sent_id"]
        if sent_id not in counter:
            counter[sent_id] = [1, [element]]
        else:
            counter[sent_id][0] += 1
            counter[sent_id][1].append(element)
    
    unique_elements = [v[1][0] for v in counter.values() if v[0] == 1]
    duplicates = [(v[0], v[1]) for k, v in counter.items() if v[0] > 1]

    return unique_elements, duplicates

def divide_neutralisation(unique_elements, duplicates):
    '''
    Place the non-unique occurences in either partial 1 or partial 2.
    This will allow for the three-way divide
    '''
    partial_1 = []
    partial_2 = []

    for _, occurrences in duplicates:
        for occurrence in occurrences:
            if len(partial_1) <= len(partial_2):
                partial_1.append(occurrence)
            else:
                partial_2.append(occurrence)

    return unique_elements + partial_1, unique_elements + partial_2


def create_lookup(replacement_data):
    """
    Create lookup replacements dictionary, where each individual token is stored together with its id and sentence id, and attached to its neutralised equivalent.
    (sent_id, token_id) : neutralized_form
    """
    lookup_replacements = {}

    for entry in tqdm(replacement_data):
        lookup_replacements[(entry["sent_id"], entry["token_id"])] = entry["neutralized_form"]
        for dependent in entry["neutralized_dependents"]:
            lookup_replacements[(entry["sent_id"], dependent["dependent_id"])] = dependent["neutralized_form"]
    
    return lookup_replacements


def swap_forms(lookup_replacements, valico_data, output_file):
    """
    Swap forms from the actual Valico dataset.
    Writes them into the output file.
    """
    with (
        open(valico_data, encoding="utf-8") as input_file,
        open("rule-based-model/data/output_dataset/" + output_file, "w", encoding="utf-8") as output_file,
        ):
        
        for sentence in parse_incr(input_file):
            sent_id = sentence.metadata.get("sent_id")

            for token in sentence:
                key = (sent_id, token["id"])
                feats = token["feats"] or {}

                if key in lookup_replacements:
                    token["form"] = lookup_replacements[key]
                    token["misc"] = "Changed=Yes"
                    feats.get("Gender") == "Neut"

            output_file.write(sentence.serialize())  


def main():
    parser = argparse.ArgumentParser(
        description="Gender neutralize data"
    )

    parser.add_argument(
        "inputdir",
        help="file path to the list of words to neutralize"
    )

    parser.add_argument(
        "valico",
        help="file path to the valico data"
    )

    parser.add_argument(
        "outdir",
        help="file path to the output"
    )

    parser.add_argument(
        "--divide",
        required = False,
        default = 'full',
        help="The type of divided wanted. Possibilities: partial1, partial2, full"
    )


    args = parser.parse_args()

    tokens_to_swap = args.inputdir
    valico_data = args.valico
    divide = args.divide.lower()
    output_file = args.outdir

    print('tokens to swap:', tokens_to_swap)
    print('valico data: ', valico_data)
    print('output_file: ', output_file)
    print('neutralization type: ', divide)

    replacements = load_replacements('data/supporting-docs/replacements.tsv')

    tokens_to_swap = load_gendered_words(tokens_to_swap)

    full_replacement_data = find_replacement(tokens_to_swap, replacements)

    unique_elements, duplicates = get_unique_occurences(full_replacement_data)

    divide_1, divide_2 = divide_neutralisation(unique_elements, duplicates)

    print(f"Length of the first divide: {len(divide_1)}")
    print(f"Length of the second divide: {len(divide_2)}")
    print(f"Length of the full data: {len(full_replacement_data)}")

    if divide == 'full':
        replacement_data = full_replacement_data
    elif divide == "partial1":
        replacement_data = divide_1
    elif divide == "partial2":
        replacement_data = divide_2

    print(f"You have picked {divide} replacement type.")

    lookup_replacements = create_lookup(replacement_data)

    swap_forms(lookup_replacements, valico_data, output_file)


if __name__ == "__main__":
    main()