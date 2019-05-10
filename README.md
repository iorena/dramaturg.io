#Dramaturg.io


#### Running the project
```bash
$ python main.py -h
usage: main.py [-h] [-s] [someargument]

positional arguments:
someargument

optional arguments:
-h, --help    show this help message and exit
-s, --story   Create a story! (default: False)
```

#### Running a module on its own:
```bash
$ python -m story.story

$ python -m scene.scene

$ python -m sequence.sequence

$ python -m adjacency_pair.adjacency_pair

$ python -m language.language
```

#### Installing hfst and omorphi
Install hfst and omorphi and syntaxmaker as per the instructions here https://github.com/mikahama/syntaxmaker
Add the location of the syntaxmaker to PYTHONPATH, for example using Conda
```bash
$ export PYTHONPATH=/home/<user_name>/.conda/envs/<env_name>/lib/python3.7/site-packages/syntaxmaker
```

