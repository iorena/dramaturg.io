grammar = """
P -> cause "G" action "O" | cause "G" event "O"
action -> "A" "P" "IE" | "A" "P" "IE" goal
event -> "E" "P" "IE" | "E" "P" "IE" goal
goal ->"G" action "O" | "G" event "O"
cause -> "IE" | "P" "IE"
"""
