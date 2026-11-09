'''
Looks up a given POS and/or deprel for data exploration purposes.
The user will be prompted to say whether they want to print the full list or not.

USAGE
-----
Lookup POS + DEPREL
python3 rule-based-model/scripts/data_exploration.py rule-based-model/data/UD_Valico/it_valico-ud-corrected_annotated.conllu --pos PROPN --deprel obj

Lookup POS
python3 rule-based-model/scripts/data_exploration.py rule-based-model/data/UD_Valico/it_valico-ud-corrected_annotated.conllu --pos PROPN

Lookup DEPREL
python3 rule-based-model/scripts/data_exploration.py rule-based-model/data/UD_Valico/it_valico-ud-corrected_annotated.conllu --deprel obj
'''

import conllu
import argparse

def load_conllu(file_path):
    """
    load the CoNLL-U file from the UD_Valico folder
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = conllu.parse(f.read())
    
    return data

def pos_lookup(data, pos = None, deprel = None):
    """
    Allows for Part-Of-Speech/deprel lookups, either combined or separately.
    """

    pos_list = []

    for sentence in data:
        sent_id = sentence.metadata.get("sent_id")

        for token in sentence:

            token_pos = token["upos"]
            token_form = token["form"]
            token_deprel = token["deprel"]

            res = (token_pos, token_form, token_deprel, sent_id)

            if pos and deprel:

                if token_pos == pos and token_deprel == deprel:
                    pos_list.append(res)
            
            elif deprel and not pos:

                if token_deprel == deprel:
                    pos_list.append(res)
            
            elif pos and not deprel:

                if token_pos == pos:
                    pos_list.append(res)
            
            else:
                raise ValueError("Neither pos nor deprel were provided.")
            
    return pos_list


def main():
    parser = argparse.ArgumentParser(
        description="Explore data"
    )

    parser.add_argument(
        "filepath",
        help="input file name"
    )

    parser.add_argument(
        "--pos",
        required = False,
        help="pos to look up for in the data"
    )

    parser.add_argument(
        "--deprel",
        required = False,
        help="deprel to look up for in the data"
    )

    args = parser.parse_args()

    input_file = args.filepath
    pos = args.pos
    deprel = args.deprel

    print('input file:', input_file)
    print('lookup pos: ', pos)
    print('lookup deprel: ', deprel)

    data = load_conllu(input_file)
    pos_list = pos_lookup(data, pos, deprel)

    print('n. of results found: ', len(pos_list))

    print('first result:', pos_list[0])

    user_answer = input(f"Do you want to print the full list of {pos, deprel}? (y/n) ")

    positive_answer = ["y", "yes"]

    if user_answer.lower() in positive_answer:
        for el in sorted(pos_list):
            print(el)

if __name__ == "__main__":
    main()