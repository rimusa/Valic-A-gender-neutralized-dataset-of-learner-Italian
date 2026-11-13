from utils.data import get_sentence_text, filter_errors
from SentenceConversion import SentenceConversion
from copy import deepcopy
from tqdm import tqdm

def get_gn_word(orig_word, words):
    for word, gn_word in words:
        if orig_word == word:
             return gn_word
    raise ValueError(orig_word)


def get_animate_samples(conll, animate_file, use_v1, hack_v2, filter):
    """
    :param conll: conll object
    :param animate_file: file containing animate noun pairs
    :param use_v1: True if sentence is annotated using UD V1.2
    :param hack_v2: True if sentence should be made into UD V2 from V1.2
    :return: list of SentenceConversion objects
    """
    with open(animate_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines = [line.strip().split("\t") for line in lines]
    print(lines)
    words = [line[0] for line in lines] + [line[1] for line in lines]

    samples = []
    for sent in tqdm(conll, total=len(conll)):
        if not filter_errors(sent) or not filter:
            changes = []
            for tok in sent:
                if tok.upos != "NOUN" and tok.upos != "PROPN" :# or 'Gender' not in tok.feats or len(tok.feats['Gender']) != 1:
                    continue
                is_masc = next(iter(tok.feats['Gender'])) == 'Masc' if tok.feats.get('Gender', None) != None else None
                if tok.form.lower() in words:
                    try:
                        convert = get_gn_word(tok.form.lower(), lines)
                    except ValueError:
                        continue
                    changes.append((int(tok.id), convert, convert, not is_masc))
            samples.append(SentenceConversion(deepcopy(sent), changes, use_v1, hack_v2))
    return samples