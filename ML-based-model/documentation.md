# Usage

All input files should be in conllu format.

## Training a model

In order to train the model, use the following command from inside the ML-based-model folder.
```bash
python src/neural-mrf.py --data [path to training data] --out_dir [path to output directory]--log_alpha 1 --lr 0.005 --wd 0.0001
```

## Running neutralization with a pretrained model

In order to run neutralization with a pretrained model, use the following command from inside the ML-based-model folder.
```bash
python src/main.py --in_files [input conllu files] --psi [path to psi .pt file] --animate_list [path to animacy list] --inc_input --get_ids --out_file [path to output_file] --part 100
```

If you wish to neutralize learner data and filter out gender errors, use the --filter tag.
```bash
python src/main.py --in_files [input conllu files] --psi [path to psi .pt file] --animate_list [path to animacy list] --inc_input --get_ids --filter --out_file [path to output_file] --part 100
```

# Credit

## Training data

The treebank used to train our model is the [UD_Italian-ParTUT](https://github.com/UniversalDependencies/UD_Italian-ParTUT).

## Code

This code is an adaptation of the code published alongside [Zmigrod et al's _Counterfactual data augmentation for mitigating gender stereotypes in languages with rich morphology_](https://github.com/rycolab/biasCDA).