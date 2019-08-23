grammar = """
S -> INS OUTS "meta" "in"
INS -> IN | IN META | IN OUT IN
OUTS -> OUT META | OUT
IN -> "in"
OUT -> "out"
META -> "meta"
"""
