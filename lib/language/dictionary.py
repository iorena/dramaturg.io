class Dictionary:
    verb_dictionary = {
        "olla": [("olla", "NOM")],
        "siirtyä": [("mennä", "ILL"), ("matkustaa", "ILL"), ("liikkua", "ILL"), ("juosta", "ILL")],
        "pitää": [("tykätä", "ELA"), ("pitää", "ELA"), ("rakastaa", "PAR")],
        "vihata": [("vihata", "PAR"), ("inhota", "PAR")],
        "hankkia": [("ostaa", "GEN"), ("hankkia", "GEN"), ("hommata", "GEN"), ("saada", "GEN")],
        "luulla": [("luulla", "PAR")],
        "kastella": [("kastella", "GEN")],
        "leikata": [("leikata", "GEN")],
        "tulla": [("tulla", "NOM")],
        "käydä": [("käydä", "ADE")],
        "tuijottaa": [("tuijottaa", "AKK")],
        "mennä": [("mennä", "ALL")],
        "vastata": [("vastata", "ALL")],
        "puhua": [("puhua", "ELA"), ("kertoa", "ELA")],
        "soittaa": [("soittaa", "ALL")],
        "ottaa": [("ottaa", "GEN")],
        "haluta": [("haluta", "GEN")],
        "kuolla": [("kuolla", "NONE")],
        "sairastua": [("sairastua", "NONE")],
        "kuulua": [("kuulua", "ALL")],
        "kuulla": [("kuulla", "PAR")],
        "arvata": [("arvata", "NONE")],
        "sanoa": [("sanoa", "GEN")],
        "höpsiä": [("höpsiä", "NONE")],
        "syntyä": [("syntyä", "NONE")],
        "nimetä": [("nimetä", "GEN")],
        "kadottaa": [("kadottaa", "GEN")],
        "etsiä": [("etsiä", "GEN")],
        "rikkoa": [("rikkoa", "GEN")],
        "siivota": [("siivota", "GEN")],
        "myydä": [("myydä", "GEN")],
        "tehdä": [("tehdä", "NONE")],
        "tietää": [("tietää", "GEN")],
        "ehdottaa": [("ehdottaa", "NOM")],
        "kysyä": [("kysyä", "GEN")],
        "ymmärtää": [("ymmärtää", "NONE")],
        "kuunnella": [("kuunnella", "NONE")],
        "hokea": [("hokea", "PAR")]
    }

    second_obj_case_dictionary = {
        "puhua": "ALL",
        "kertoa": "ALL"
    }

    noun_dictionary = {
        "disappointment": ["surullinen", "pettynyt"],
        "gratification": ["tyytyväinen"],
        "happy_for": ["onnellinen", "iloinen"],
        "kyllä": ["kyllä", "joo", "aivan", "niin"],
        "mitä": ["mitä", "häh", "täh", "anteeksi"],
        "great": ["mahtava", "loistava", "upea"],
        "good": ["hyvä", "mainio", "kaunis"],
        "okay": ["kelvollinen", "mukiinmenevä"],
        "bad": ["huono", "onneton", "kurja"],
        "horrible": ["surkea", "hirveä"],
        "pahus": ["pahus", "harmi", "sääli"],
        "hienoa": ["mainiota", "hienoa", "hyvä"],
        "moi": ["terve", "moi", "hei"],
        "sunny": ["aurinkoinen"],
        "cloudy": ["pilvinen"],
        "rainy": ["sateinen"],
        "stormy": ["myrskyinen"],
        "alive": ["elossa"]
    }
    reversed_verb_dictionary = {
        "siirtyä": [("viedä", "ILL"), ("kuljettaa", "ILL")],
        "hankkia": [("ostaa", "GEN"), ("hankkia", "GEN"), ("hommata", "GEN")]
    }

    evaluations_dictionary = {
        "great": ["vau", "loistavaa", "mahtavaa"],
        "good": ["hyvä", "hienoa", "jee"],
        "okay": ["okei", "selvä", "jep"],
        "bad": ["pahus", "hitto", "eikä"],
        "horrible": ["ei helvetti", "perkele"]
    }

    valence_dictionary = {
        "NEWS": ["minulla on huonoja uutisia", "minulla on hyviä uutisia"],
        "INSULT": ["senkin pahanilmanlintu", "hyvä kuulla"],
        "SORRY": ["olen pahoillani", "eikö olekin hienoa ?"],
        "WORRY": ["älä huoli", "pelkään pahoin, että"],
        "LUCK": ["onneksi", "valitettavasti"],
        "FEAR": ["pelkäsinkin jotain tällaista", "toivoinkin, että näin olisi"],
        "SERIOUS": ["oletko tosissasi ?", "ihanko totta ?"],
        "TELL": ["miksi kerrot tästä vasta nyt ?", "kyllä minä sen tiesin"],
        "FRUSTRATION": ["se tästä vielä puuttuikin", "olisit heti sanonut"]
    }

    explicatives_dictionary = {
        "pos": {
            "tosi": [1, 1, 0],
            "erittäin": [0.7, 0.7, 0.2],
            "hemmetin": [-0.5, 0.5, 0.5],
            "pirun": [-1, 0.5, 1],
            "niin": [-0.5, 0, 0],
            "kyllä": [0, 0.5, 0.2],
            "sitten": [-0.5, 0, 0.2]
        },
        "neg": {
            "yhtään": [-1, 1, 1],
            "kovin": [0, 0.5, 0]
        }
    }
