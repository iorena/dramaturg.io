#dramaturg.io - Scripts
This folder contains two parsers designed to parse action types and project words from CoNLL-U formated input. The scripts have been designed to work with CoNLL-U files generated with the tool [Turku-neural-parser-pipeline](https://github.com/TurkuNLP/Turku-neural-parser-pipeline).

## action\_type\_parser.pl
Generates [action types](https://github.com/iorena/dramaturg.io/blob/text_input/data/action_types.csv). Give CoNLL-U files as arguments:
```
./action_type_parser.pl file1.conllu file2.conllu ... fileN.conllu > action_types.csv
```

# project\_words\_parser.pl
Generates subject-verb-object triplets usable as project words. Give CoNLL-U files as arguments:
```
./project_words_parser.pl file1.conllu file2.conllu ... fileN.conllu > project_words.csv
```

