"""
Usage
-----

INCORRECT DATA: 
python3 rule-based-model/scripts/find_gendered_tokens.py rule-based-model/data/UD_Valico/it_valico-ud-test.conllu noun_dependents_incorrect.json

WITH FILTERING OF GENDER ERRORS:
python3 rule-based-model/scripts/find_gendered_tokens.py rule-based-model/data/UD_Valico/it_valico-ud-test.conllu noun_dependents_incorrect_filtered.json --filter

CORRECT DATA: 
python3 rule-based-model/scripts/find_gendered_tokens.py rule-based-model/data/UD_Valico/not-to-release/corrected/it_thvalico-ud-test.conllu noun_dependents_correct.json

WITH FILTERING OF GENDER ERRORS:
python3 rule-based-model/scripts/find_gendered_tokens.py rule-based-model/data/UD_Valico/not-to-release/corrected/it_thvalico-ud-test.conllu noun_dependents_correct_filtered.json --filter
"""

import conllu
import pandas as pd
import json
import argparse
import re

def load_conllu(file_path):
    """
    load the CoNLL-U file from the UD_Valico folder
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = conllu.parse(f.read())
    
    return data

def filter_errors(sentence):
    '''
    Filters sentences containing a gender error by selecting
    <> signs around the error tag
    [^>] any signs before / after G
    G indicates a gender error
    '''
    err = sentence.metadata.get("err")
    pattern = r"<([^>]*G[^>]*)>"  
    result = re.findall(pattern, err)
    if result:
        return True #this sentence should be filtered
    return False

def filter_past_partpciple(pp_token, sentence):
    """
    Given a past participle token, checks whether it is attached to AUX avere.
    Returns false if avere.
    """
    pp_token_id = pp_token["id"]

    for token in sentence:

        head = token["head"]
        lemma = token["lemma"]
        upos = token["upos"]

        if head == pp_token_id and lemma == "avere" and upos == "AUX":
            return False
    return True

def is_relevant_dependent(token, sentence):
    """
    Select tokens that are relevant for gender agreement.
    Also stole my soul and will to live.

    Explanation of Conditions for each relevant POS:

    ADJ
    Included all adj, but could be easily filtered if we notice irrelevant tokens.

    NOUN
    Only included nouns if deprel is "appos":
        appos: noun directly modifying another noun, e.g. "Il mio Fratello, <l'insegnante>, è arrivato"
    Complex cases:
        conj: had initially also had "conj" as a deprel condition, but removed it, as hopefully the list of human animate will pick up on these cases
        nmod: had thought of nmon, but it would pick up cases like "un uomo senza paura", where we dont really want paura to be picked up
    
    VERB 
    Only included verbs if verbform is "Part" and deprel is in {"acl", "acl:relcl", "xcomp"}
        acl: clausal modifier of noun, like "la ragazza <arrivata>"
        acl:recl: relative clause modifier, like "la ragazza che è <arrivata>"
        xcomp: open clausal complement, like "sono restato <intontito>". Full definition: https://universaldependencies.org/u/dep/xcomp.html

    PRON + DET
    Excluded the following PronType:
        excl: exclamative pronouns "<che>" bello"
        neg: negative pronoun, basically negation
    Complex cases:
        rel: relative pronouns unless it starts with "qu" 
            "l'umomo <che> lavora all'università" --> excluded
            "il ragazzo <il quale> lavora al supermecato è gentile" --> included
        int: interrogative pronouns unless it starts with "qu"
            "chi lo sai?" --> excluded
            "quanti studenti hanno participato?" --> included    

    """

    feats = token["feats"] or {}
    upos = token["upos"]
    deprel = token["deprel"]
    form = token["form"].lower()

    if token["lemma"]:
        lemma = token["lemma"].lower()
    else:
        lemma = ""

    if upos == "ADJ" and feats.get("Gender"):
        return True

    if upos == "NOUN" and deprel in {"appos"}: #could add more if needed, e.g. conj?
        return True
    
    if upos == "VERB" and feats.get("VerbForm") == "Part" and deprel in {"acl", "acl:relcl", "xcomp", "cop"}:
        if filter_past_partpciple(token, sentence):
            return True
    
    if (upos in {"PRON", "DET"} and feats.get("PronType") in {"Rel", "Int"} and not (form.startswith("qu") or lemma.startswith("qu"))):
        return False
        
    if upos in {"PRON", "DET"} and feats.get("PronType") not in {"Exc", "Neg"}: #could add more if needed
        return True
    
    return False

def is_relevant_head(head_token, instance, sentence):
    """
    Select head that is relevant for agreement

    This time, I first check for deprel, then for upos, because deprel is the decisive factor for nouns' heads.

    Explanation of conditions to be selected as a relevant head:
        nsubj: nominal subject, which includes adj/nouns, like "la ragazza è <bella> / è <dottoressa>"
        nsubj:pass: nominal subject for passive, like "le mele sono <comprate>"
        csubj: clausal subject, like "i amici che sono <partiti>"
    
    Note that I manually checked and there are very few cases of csubj/nsubj, but still included because it could be relevant for other datasets
    """
    if instance["deprel"] not in {"nsubj", "nsubj:pass", "csubj"}:
        return False

    feats = head_token["feats"] or {}
    upos = head_token["upos"]

    if upos == "ADJ" and feats.get("Gender"):
        return True

    if upos == "VERB" and feats.get("VerbForm") == "Part":
        if filter_past_partpciple(head_token, sentence):
            return True

    if upos == "NOUN":
        return True
    
    return False

def build_token_info(token):
    """
    Build the dictionary containing information about the token.
    Not sure yet which bit we need, so I put everything that sounded remotely relevant :)
    """


    token_info = {"id": token["id"],
                "form": token["form"],
                "lemma" : token["lemma"],
                "upos": token["upos"],
                "head": token["head"],
                "deprel": token["deprel"],
                }

    if token["feats"]:
        token_info["number"] =  token["feats"].get("Number")
    else:
        token_info["number"] = None
        
    return token_info

def get_noun_instances(sentence, noun_form:str):
    """
    Checks if a sentence contains a given human animate noun.
    Retrieves the token information for each occurence of the noun
    and stores it under "instances". Also retrieves the sentence ID.
    """

    sent_id = sentence.metadata.get("sent_id")
    
    noun_instances = {
        "sent_id": sent_id,
        "instances": []
    }

    for token in sentence:
        if token["form"].lower() == noun_form and token["upos"] in {"NOUN", "PROPN"}:
            noun_info = build_token_info(token)
            noun_instances['instances'].append(noun_info)

    return noun_instances 

def get_dependencies(sentence, noun_instances:dict):
    """
    Based on the instances of a given noun, find:
    1. Dependents: the tokens that depend on the given noun, if is_relevant_dependent
    2. Head: the head of the given noun, if is_relevant_head
    ONLY retrieves tokens if they are relevant for gender
    """

    for instance in noun_instances["instances"]:

        instance["dependents"] = [] #create a new dictionary entry for each instance

        for token in sentence:

            #DEPENDENTS
            if token["head"] == instance["id"]: #check if it is a dependent
                if is_relevant_dependent(token, sentence): #if dependent is relevant for agreement
                    token_info = build_token_info(token) #get the info of the token
                    instance["dependents"].append(token_info) #append it to dependent list
            
            #HEAD 
            if token["id"] == instance["head"]: #same logig as above but reversed
                if is_relevant_head(token, instance, sentence):
                    token_info = build_token_info(token)
                    instance["head_token"]= token_info #creates a new dictionary entry
    
    return noun_instances

def apply_get_dependencies(data, gendered_nouns:list, filter = True):
    """
    Find dependents and heads for each human noun in gendered_nouns, in each sentence
    First, applies get_noun_instances to check for human noun and retrieve info.
    Then, applies get_dependencies to get dependents and head relevant for gender agr.
    """
    noun_dependencies = []
    count_filtered_sentences = 0

    for sentence in data:

        if filter:

            if filter_errors(sentence):
                count_filtered_sentences += 1
                continue

            else:
                for noun in gendered_nouns:
                    noun_instances = get_noun_instances(sentence, noun)
                    if noun_instances["instances"]:
                        dependents_and_head = get_dependencies(sentence, noun_instances)
                        noun_dependencies.append(dependents_and_head)
        else:
            for noun in gendered_nouns:
                    noun_instances = get_noun_instances(sentence, noun)
                    if noun_instances["instances"]:
                        dependents_and_head = get_dependencies(sentence, noun_instances)
                        noun_dependencies.append(dependents_and_head)

    return noun_dependencies, count_filtered_sentences

def load_excel(file_path, sheet):
    """
    Return loaded excel file containing human nouns
    """
    human_noun_list = pd.read_excel(file_path, sheet_name=sheet)
    return human_noun_list


def to_json(dependents:list, output:str):
    """
    Creat json file under output_data directory
    output is the name of the file.
    """
    with open('rule-based-model/data/gendered_tokens/' + output, 'w') as f:
        json.dump(dependents, f, indent=4)


def main():
    parser = argparse.ArgumentParser(
        description="Find gendered words"
    )

    parser.add_argument(
        "input",
        help="input file name"
    )

    parser.add_argument(
        "output",
        help="output file name"
    )

    parser.add_argument(
        "--filter",
        action="store_true",
        help="Filter erroneous sentences"
    )

    args = parser.parse_args()

    print('input file:', args.input)
    print('output file:', args.output)
    print('filtering: ', args.filter)

    human_noun_list = load_excel("data/supporting-docs/rules.xlsx", "human_nouns")

    gendered_nouns = human_noun_list["gendered_form"]

    data = load_conllu(args.input)

    noun_dependents, count_filtered_sentences = apply_get_dependencies(data, gendered_nouns, filter = args.filter)

    print(f"Number of sentences filtered: {count_filtered_sentences}")

    print(f"Exporting to json under the name {args.output}.")

    to_json(noun_dependents, args.output)

if __name__ == "__main__":
    main()
