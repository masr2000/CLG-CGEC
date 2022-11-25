from typing import Union, Optional

from segmentor import seg_dec
import re

class Augmentor:
    def __init__(self):
        # 规则函数：以单下划线开头
        self.rules = [name for name in dir(self) if re.match("^_[a-zA-Z]", name) and callable(getattr(self, name))]

    @seg_dec
    def transform(self, sent: Union[list, str]) -> tuple[list, list]:
        results, rules = [], []
        for rule in self.rules:
            result = getattr(self, rule)(sent)
            if result is not None:
                results.append(result)
                rules.append(rule)
        return results, rules