grammar = """
P -> cause goal
goal ->"G" action "O" | "G" event "O" | "G" action "O" goal
action -> "A" "P" "IE"
event -> "E" "P" "IE"
cause -> "IE" | "P" "IE"
"""
