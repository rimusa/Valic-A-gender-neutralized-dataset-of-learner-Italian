# Valicə
### A gender-neutralized dataset of learner Italian

This repo contains the Valicə dataset and related code, presented at the 7th Workshop on Gender Bias in Natural Language Processing (GeBNLP).
The current file contains an introduction to the dataset. If you would like a more in-depth explanation, feel free to check out the paper and the datacard.

### About

Investigations of gender-neutral and non-binary language in Romance language often fail to take into account learner language.
There is a lack of material to study how grammatical error correction models handle gender-neutral language which uses new forms or morphemes.
The Valicə dataset is a gender-neutralized version of [the Valico treebank](https://universaldependencies.org/treebanks/it_valico/index.html), containing Italian learner texts and their corrections.
It is accompanied by code that can be used to gender-neutralize Italian sentences, whether they are grammatically correct or incorrect.
Two different systems can be used to identify which tokens should be neutralized: a rule-based system and a machine learning system.
The token swap is rule-based, using the neomorphemes -ə and -ɜ to signal singular and plural gender-neutrality.
The Valicə dataset can be used to evaluate or train language learning applications for learners of Italian.

### Dataset

TODO

### Citing Valicə

If you use the Valicə dataset, please cite the paper describing it.
The standard citation can be found below.

> Céline Leuzinger, Caroline Grand-Clement, Ricardo Muñoz Sánchez, and Tom Södahl Bladsjö. 2026. Valic\textipa{@}: A gender-neutralized dataset of learner Italian. In Proceedings of the 7th Workshop on Gender Bias in Natural Language Processing (GeBNLP), Hengqin, China. Association for Computational Linguistics.
