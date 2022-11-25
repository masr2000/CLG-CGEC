import random
import re
from typing import Union, Optional

import synonyms

from augmentor import Augmentor

DEBUG = False

class RedundantComponent(Augmentor):
    def __init__(self, n_word_probs=(0.5, 0.3, 0.1, 0.1), k_probs=(0.15,) * 3 + (0.1,) * 4 + (0.05,) * 3):
        super(RedundantComponent, self).__init__()
        self.n_word_probs = n_word_probs
        self.k_probs = k_probs

    def _redundant_component(self, sent: Union[list, str]) -> list:
        output = []
        valid_indices = [i for i, (word, pos) in enumerate(sent) if re.match(r"[vadcp]", pos)]
        n_word = random.choices(range(1, len(self.n_word_probs) + 1), weights=self.n_word_probs)[0]
        select_indices = set(random.sample(valid_indices, k=min(n_word, len(valid_indices))))
        # print(valid_indices, n_word, select_indices)
        for i, (word, pos) in enumerate(sent):
            origin = (word, pos)
            if i in select_indices:
                rand = random.random()
                word_synonyms, _ = synonyms.nearby(word, size=len(self.k_probs) + 1)
                # print(word, word_synonyms)
                if len(word_synonyms) <= 1:
                    continue
                synonym = random.choices(word_synonyms[1:], weights=self.k_probs)[0]
                transform = (f"(I: {synonym})", pos) if DEBUG else (synonym, pos)
                if rand < 0.5:
                    output.append(transform)
                output.append(origin)
                if rand >= 0.5:
                    output.append(transform)
            else:
                output.append(origin)
        return output
