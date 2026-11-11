# Data Card

This datacard is based on the template used to document the resources that form part of SuperLim.
Said template can be found [here](https://github.com/spraakbanken/SuperLim).


## 1. Identifying Information

### General Information

- **Title:** Valicə
- **Subtitle:** A gender-neutralized dataset of learner Italian
- **Created by:** Céline Leuzinger, Caroline Grand-Clement, Ricardo Muñoz Sánchez, and Tom Södahl Bladsjö
- **Publisher(s):** N/A
- **License(s):** TODO
- **Funded by:** N/A
- **Link(s)/permanent identifier(s):**
  - [https://github.com/rimusa/Valic-A-gender-neutralized-dataset-of-learner-Italian](https://github.com/rimusa/Valic-A-gender-neutralized-dataset-of-learner-Italian)
  - [https://aclanthology.org/2026.gebnlp-1.2/](https://aclanthology.org/2026.gebnlp-1.2/)


### Abstract

Investigations of gender-neutral and non-binary language in Romance languages often fail to take into account learner language.
There is a lack of material to study how grammatical error correction models handle non-binary language which uses new forms or morphemes.
In this paper, we offer Valicə, a gender-neutralized version of the Valico treebank, containing Italian learner texts and their corrections.
We present the procedure to gender-neutralize Italian sentences, both grammatically correct and incorrect.
We implement two different systems to identify which tokens should be neutralized: a rule-based system and a machine learning system, both of which prove equally efficient.
The token swap is rule-based, using the neo-morphemes -ə and -ɜ to signal singular and plural gender-neutrality.
The Valicə dataset can be used to evaluate or train language learning applications for learners of Italian.



### Citation

> Céline Leuzinger, Caroline Grand-Clement, Ricardo Muñoz Sánchez, and Tom Södahl Bladsjö. 2026. Valicə: A gender-neutralized dataset of learner Italian. In Proceedings of the 7th Workshop on Gender Bias in Natural Language Processing (GeBNLP), pages 7-20 Hengqin, China (remote). Association for Computational Linguistics.


## 2. Usage	

- **Key applications:** Evaluate whether grammatical correction/detection systems of Italian learner texts accept non-binary language as a valid way to use the language.
- **Intended task(s)/usage(s):** Grammatical error correction and/or detection.
- **Recommended evaluation measures:** GLEU, ERRANT, and Scribendi scores. These metrics are being suggested as they were the ones used for [the MultiGEC-2025 shared task](https://spraakbanken.github.io/multigec-2025/).
- **Dataset function(s):** Diagnostics
- **Recommended split(s):** Test split only


## 3. Data	

- **Primary data:** Text
- **Language:** Italian

### Dataset Description

The dataset contains several versions of both the original learner texts as well as their correction hypotheses.
Two different models were used with two different settings for the data.

One of the models is a rules-based model that does token-level swap in order to insert neo-morphemes into the data.
The other model does counterfactual data augmentation using a Markov random field.
More information on both of these models can be found on [the dataset paper](https://aclanthology.org/2026.gebnlp-1.2/).

The data was produced with two setups.
In the _filtered_ setup, we removed all sentences that had grammatical errors regarding gender in order to avoid any confounding factors.
The _unfiltered_ setup used the data as-is with the idea that this might reflect noisier real-life settings.


### Dataset in numbers

_Learner texts_:
in the filtered setting, 197 sentences are neutralized for the rule-based model, yielding
a total of 632 non-binary tokens.
For the machine learning-based model, 195 sentences are neutralized, for a total of 662 non-binary tokens.
In the unfiltered setting, 271 sentences are neutralized for the rule-based model against 297 for the machine learning-based model.
This yields a total of 918 tokens for the rule-based system and 1000 for the machine learning-based system.

_Corrected texts_: in the filtered settings, 194 sentences are gender neutralized for the rule-based model, yielding a total of 632 non-binary tokens.
The machine learning-based model neutralizes a total of 189 sentences and 662 non-binary tokens.
In the unfiltered setting, the number of sentences rises to 266 for both models, yielding 913 non-binary tokens for the rule-based system and 989 for the machine learning-based model.


### Nature of the content

Valicə is a dataset of Italian learner data along with correction hypotheses that includes non-binary neoforms.
This dataset is meant to evaluate whether language learning systems, such as grammatical error correction tools, accept non-binary language.
The dataset can also be used to fine-tune said systems to ensure language learners can express their gender identities in their target language without being censored by the tools that are meant to help them.


### Format

#### Datasets
The dataset is available in both CoNLL-U format (for the original texts) and as text files (for the corrected versions), with one sentence per line.


#### Supporting Documents
The supporting documents folder contains three TSV files with the original words and their substitutions.
It also contains an XLSX file with comments about these rules and substitutions.


### Data source(s)

The texts were retrieved from [the Valico treebank](https://universaldependencies.org/treebanks/it_valico/index.html) of Italian learner texts.


### Data selection and filtering

There are two versions of the Valicə dataset, one that has all texts included in the Valico treebank and one version that has been filtered to remove texts with gender-related errors.


## 4. Ethics and Caveats	

### Ethical considerations

This paper deals with how people use language to express their identities in ways that diverge from the norm.
However, the ways in which people use gender-neutral and/or non-binary language can vary greatly both through time and across different groups and individuals.
As such, we are aware that we risk presenting this kind of language as if it were monolithical, rather than an ever-evolving way of speaking.


### Things to watch out for

The dataset relies on UD annotation.
The starting point for token identification, in both systems, is human animacy and proper nouns, meaning we only identify third-person referents to neutralize.
The list of human animates and proper nouns used is crafted manually, a task which is not easily scalable.
In regards to the gender-neutralization, we make decisions about the rules to implement, which represent only one way of making gender-neutral or non-binary language in Italian.


### 5. About Documentation	

- **Data last updated:** 2026-11-11
- **Which changes have been made, compared to the previous version:** N/A
- **Access to previous versions:** N/A
- **This document created:** 2026-11-11
- **This document last updated:** 2026-11-11
- **Where to look for further details:** [The paper that introduced the Valicə dataset](https://aclanthology.org/2026.gebnlp-1.2/) 
- **Documentation template version:** [1.0](https://github.com/spraakbanken/SuperLim/blob/main/documentation_sheet_template_v1.0.tsv)

