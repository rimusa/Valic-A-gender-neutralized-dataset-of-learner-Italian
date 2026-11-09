import argparse
from utils.conll import load_sentences

def get_args():
    """
    :return: command-line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--coref_file', required=True, help='Input coref file')
    parser.add_argument('--conllu_file', required=True, help='Input conllu file')
    return parser.parse_args()

def main():
    opt = get_args()
    corefs = []
    with open(str(opt.coref_file) + ".txt", "r", encoding="utf-8") as coref_file:
        for line in coref_file:
            if len(line.split()) > 0 and line[0] != "#":
                corefs.append(line.split())

    conllu_file = opt.conllu_file
    annotated = []
    with open(conllu_file + ".conllu", "r", encoding="utf-8") as f:
        # Work in batches of 100,000 sentences to avoid memory issues
        not_empty = True
        while not_empty:
            # Load sentences
            print("    Loading partition...")
            conll_sents, not_empty = load_sentences(10000, f)
            
            for coref, conll in zip(corefs, conll_sents):
                ref_id = 0
                conll_id = 0
                section = False
                while conll_id < len(conll._tokens):
                    tok = conll._tokens[conll_id]
                    if len(tok.id.split("-")) > 1:
                        conll_id += 2
                    if "{" in coref[ref_id]:
                        ref_id += 1
                        section = True
                    if section:
                        tok = conll._tokens[conll_id]
                        tok.misc["OfInterest"] = {"Yes"}
                        print(tok.misc)
                        if "}" in coref[ref_id]:
                            section = False
                    ref_id += 1
                    conll_id += 1
                annotated.append(conll.conll())

    with open(conllu_file + "_annotated.conllu", "w", encoding="utf-8") as outfile:
        outfile.write("\n\n".join(annotated) + "\n\n")
                    
if __name__=="__main__":
    main()