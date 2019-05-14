action_grammar = """
S -> "ter" SEQ | SEQ
SEQ -> SEQ "ilm" | "ilm" | "kys" | SEQ "kys"
"""
perception_grammar = """
S -> "hav" | "hav" LAA
LAA -> "kys" | "kys" LAA
"""
