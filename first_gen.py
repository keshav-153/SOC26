import random

class CodeGenerator:
    def __init__(self):
        self.symbol_table = ["x", "y", "z"]
        self.depth = 0
        self.max_depth = 5

    def generate(self, non_terminal):
        # Prevent infinite recursive expansion by forcing terminal branches
        if self.depth > self.max_depth:
            if non_terminal == "MIF": return "x = 1"
            if non_terminal == "EXPR": return "1"
            if non_terminal == "TERM": return "2"

        if non_terminal == "STMT":
            rule = random.choice(["MIF", "UIF"])
            return self.generate(rule)

        elif non_terminal == "MIF":
            self.depth += 1
            choices = [
                lambda: f"if {self.generate('EXPR')} then {self.generate('MIF')} else {self.generate('MIF')}",
                lambda: f"{random.choice(self.symbol_table)} = {self.generate('EXPR')}"
            ]
            # Weight probabilities to prefer assignment as depth increases
            weights = [0.3, 0.7] if self.depth > 3 else [0.6, 0.4]
            chosen_func = random.choices(choices, weights=weights)[0]
            res = chosen_func()
            self.depth -= 1
            return res

        elif non_terminal == "EXPR":
            self.depth += 1
            rule = random.choice(["EXPR+TERM", "TERM"])
            if rule == "EXPR+TERM":
                res = f"{self.generate('EXPR')} + {self.generate('TERM')}"
            else:
                res = self.generate("TERM")
            self.depth -= 1
            return res

        elif non_terminal == "TERM":
            return random.choice([lambda: random.choice(self.symbol_table), lambda: str(random.randint(1, 100))])()
