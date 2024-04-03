# Author: Harsh Kohli
# Date Created: 31-08-2023

class Condition:

    def __init__(self, cond_type, value1, pos_text, neg_text, value2=None):
        self.cond_type = cond_type
        self.value1 = value1
        self.value2 = value2
        self.pos_text = pos_text
        self.neg_text = neg_text
