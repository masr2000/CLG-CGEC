import random
import re
from typing import Optional

from augmentor import Augmentor

delimiters = "，。！？：；.,!?:;"
numerals = "一二三四五六七八九0123456789"

class ImproperLogicality(Augmentor):
    def __init__(self):
        super(ImproperLogicality, self).__init__()

    def _insert_negation(self, sent: list) -> Optional[str]:
        trigger_words = ["避免", "防止", "杜绝"]
        escape_words = ["无法", "不能"]
        verbs = ["受到", "接受", "使用", "发生", "出现", "遭", "被", "遇见", "忘记", "丢失", "遗忘", "传播", "泄露"]
        text = "".join(map(lambda x: x[0], sent))
        search = re.search(f"(?<!{'|'.join(escape_words)})({'|'.join(trigger_words)})[^{delimiters}]*?({'|'.join(verbs)})", text)
        if search is not None:
            start, end = search.span()
            verb_length = len(search.group(2))
            return text[:end - verb_length] + "不" + text[end - verb_length:]
        return None

    def _insert_absolute(self, sent: list) -> Optional[str]:
        trigger_words = ["往往", "时常", "经常", "偶尔", "每每", "不时", "常常", "通常", "有时"]
        replace_words = ["总", "总是", "一定"]
        text = "".join(map(lambda x: x[0], sent))
        search = re.search(f"({'|'.join(trigger_words)})(?![{delimiters}])", text)
        if search is not None:
            select_word = random.choice(replace_words)
            trigger_word = search.group(1)
            start, end = search.span()
            return text[:start] + select_word + text[start + len(trigger_word):]
        return None

    def _replace_coordinate(self, sent: list) -> Optional[str]:
        text = "".join(map(lambda x: x[0], sent))
        candidates = ["和", "以及", "或"]
        search = re.search(f"、[^{delimiters}]+?等", text)
        if search is not None:
            start, end = search.span()
            return text[:end - 1] + random.choice(candidates) + text[end:]
        search2 = re.search(f"、[^{delimiters}]+?以及", text)
        if search2 is not None:
            start, end = search2.span()
            return text[:end - 2] + "等" + text[end:]
        return None

    def _replace_numeral(self, sent: list) -> Optional[str]:
        text = "".join(map(lambda x: x[0], sent))
        trigger_words = ["降低", "减少", "下降", "减低", "减"]
        search = re.search(f"({'|'.join(trigger_words)})(一半|[{numerals}]分之[{numerals}]|[0-9.]+%)", text)
        if search is not None:
            start, end = search.span()
            # print(search)
            scope = search.group(2)
            if scope == "一半":
                replace_word = "一倍"
            elif re.match(f"^[{numerals}]分之[{numerals}]$", scope):
                replace_word = f"{scope[0]}倍"
            elif (match := re.match(f"^([0-9.]+)%$", scope)):
                try:
                    str_num = match.group(1)
                    num = float(str_num) if "." in str_num else int(str_num)
                    while num < 100:
                        num *= 10
                    print(num)
                    replace_word = f"{num}%"
                except ValueError:
                    return None
            else:
                raise NotImplementedError
            return text[:end - len(scope)] + replace_word + text[end:]
        return None