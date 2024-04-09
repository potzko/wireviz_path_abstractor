import re

dead = [
    (re.compile(r" "), "space"),
    (re.compile(r"\n"), "space"),
    (re.compile(r"  "), "space"),
    (re.compile(r"\/\/.*?\n"),  "comment"),
    (re.compile(r"\/\*.*?\*\/"),  "comment"),
]

spec = [
    (re.compile(r"connections"), "connections"),
    (re.compile(r"virtual_points"), "virtual_points"),
    (re.compile(r"distances"), "distances"),
    (re.compile(r"[_a-zA-Z][_a-zA-Z0-9]*"), "node"),
    (re.compile(r"{"), "{"),
    (re.compile(r"}"), "}"),
    (re.compile(r"\("), "("),
    (re.compile(r"\)"), ")"),
    (re.compile(r","), ","),
    (re.compile(r"\b\d+(\.\d+)?\b"), "distance"),
]

class tokenizer:
    def __init__(self, text) -> None:
        self.index = 0
        self.text = text
        
    @property
    def remaining_text(self):
        return self.text[self.index:]

    def eat(self, token_type = None):
        ret = self.peak()
        if token_type:
            if token_type != ret[0]:
                raise Exception(f"expected token of type {token_type}, found the token {ret[1]} of type {ret[0]}")
        self.index += len(ret[1])
        return ret

    def peak(self):
        self.strip_dead()
        if self.remaining_text == "":
            return ("EOF", "")
        for reg, token_type in spec:
            if reg.match(self.remaining_text):
                return token_type, reg.match(self.remaining_text).group(0)
        raise Exception(f"could not tokenize: {self.remaining_text}")
    
    def strip_dead(self):
        flag = True
        while flag:
            flag = False
            for reg, token_type in dead:
                if reg.match(self.remaining_text):
                    flag = True
                    self.index += len(reg.match(self.remaining_text).group(0))
    
    def optional_eat(self, token_type):
        if self.peak_type() == token_type:
            return self.eat()
        return None

    def peak_type(self):
        return self.peak()[0]