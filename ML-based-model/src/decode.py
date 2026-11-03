import pandas as pd
from utils.data import load_replacements, get_gn_word


def decode_word(token):
    form = token.form
    lemma = token.lemma
    root = token.form if form[-1] in 'aeiouAEIOU' else lemma
    replacements = load_replacements("../data/supporting-docs/replacements.tsv")
    new_form = get_gn_word(form.lower(), replacements)
    if not new_form:
        num = token.feats.get("Number")
        if not num or (form[-1] not in 'aeiouAEIOU' and lemma[-1] not in 'aeiouAEIOU'):
            new_form = form
        else:
            if "Sing" in num:
                new_form = root[:-1] + "ə"
            elif "Plur" in num:
                new_form = root[:-1] + "ɜ"    
   
    if form.isupper():
        new_form = new_form.upper()
    elif form[0].isupper():
        new_form = new_form.capitalize()

    token.misc["Changed"] = {"No"} if new_form == form else {"Yes"}
        
    return new_form, token.misc 
