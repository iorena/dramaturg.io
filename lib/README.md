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

As of now omorphi applies wrong ownership for its files in `/usr/local/share/hfst`.
Fix ownership and permissions so that python can access them. ie.
```bash
$ chown <username>:<usergroup> -R /usr/local/share/hfst
$ chmod a+rX /usr/local/share/hfst
```

#### Adding embeddings model
Download Turku NLP word embeddings binary model from here: http://dl.turkunlp.org/finnish-embeddings/ and put it into /data.


#### Adding lines into CSV files
You can add new sequence and action types by editing the files sequence/sequence_types.csv, sequence/expansion_types.csv and language/action_types.csv

Make sure each new sequence is handled in both sequence_types and expansion_types and each new action is added to action_types.csv
