import random
import re
from typing import Optional

from augmentor import Augmentor

delimiters = "，。！？：；.,!?:;"

class StructuralConfusion(Augmentor):
    def __init__(self):
        super(StructuralConfusion, self).__init__()
        self.mixed_patterns = [
            # 是...的结果 & 是由于... -> 是由于...的结果
            (("是", "的结果"), ("是由于", f"[{delimiters}]"), (1, 0)),
            # 以...为目的 & 是为了... -> 是为了...为目的
            (("以", "为目的"), ("是为了", f"[{delimiters}]"), (1, 0)),
            # 对于...问题 & 在...问题上 -> 对于...问题上
            (("对于", "问题"), ("在", "问题上"), (0, 1)),
            # 原因是... & 是由...造成的 -> 原因是...造成的
            (("原因是", f"[{delimiters}]"), ("是由", "造成的"), (0, 1)),
            # 靠的是... & 是靠...取得的 -> 靠的是...取得的
            (("靠的是", f"[{delimiters}]"), ("是靠", "取得的"), (0, 1)),
            # 本着...的原则 & 以...为原则 -> 本着...为原则
            (("本着", "的原则"), ("以", "为原则"), (0, 1)),
            # 成分是... & 由...配置而成 -> 成分是...配制而成
            (("成分是", f"[{delimiters}]"), ("由", "配置而成"), (0, 1)),
            # 以...为幌子 & 打着...的幌子 -> 打着...为幌子
            (("以", "为幌子"), ("打着", "的幌子"), (0, 1)),
            # 关键在于... & ...是十分重要的 -> 关键在于...是十分重要的
            (("关键在于", f"[{delimiters}]"), (f"[{delimiters}]", "是十分重要的"), (0, 1)),
            # 分为...部分 & 由...部分组成 -> 分为...部分组成
            (("分为", "部分"), ("由", "部分组成"), (0, 1)),
            # 有...部分 & 由...部分组成 -> 有...部分组成
            (("有", "部分"), ("由", "部分组成"), (0, 1)),
            # 围绕... & 以...为中心 -> 围绕...为中心
            (("围绕", f"[{delimiters}]"), ("以", "为中心"), (0, 1)),
            # 从...出发 & 以...为出发点 -> 从...为出发点
            (("从", "出发"), ("以", "为出发点"), (0, 1)),
            # 之所以... -> 之所以...的原因
            (("之所以", f"[{delimiters}]"), (f"[{delimiters}]", "的原因"), (0, 1)),
            # 听到...消息 & ...消息传来 -> 听到...消息传来
            (("听到", "消息"), (f"[{delimiters}]", "消息传来"), (0, 1)),
        ]
        self.mixed_patterns_2 = [
            (["是由于", "是因为", "原因是"], ["的原因", "的结果", "决定的", "造成的"]),
            (["高达", "长达"], ["之多", "之久"]),
        ]

    def _mix_pattern_1(self, sent: list) -> Optional[str]:
        text = "".join(map(lambda x: x[0], sent))
        for (pattern1, pattern2, (index1, index2)) in random.sample(self.mixed_patterns, k=len(self.mixed_patterns)):
            assert (index1, index2) in [(0, 1), (1, 0)]
            search = re.search(f"{pattern1[0]}[^{delimiters}]*?{pattern1[1]}", text)
            if search is not None:
                start, end = search.span()
                if index1 == 0:
                    end2 = end - 1 if text[end - 1] in delimiters else end
                    return f"{text[:end - len(pattern1[1])]}{pattern2[1]}{text[end2:]}"
                else:
                    start2 = start + 1 if text[start] in delimiters else start
                    return f"{text[:start2]}{pattern2[0]}{text[start + len(pattern1[0]):]}"
            search2 = re.search(f"{pattern2[0]}[^{delimiters}]*?{pattern2[1]}", text)
            if search2 is not None:
                start, end = search2.span()
                if index2 == 0:
                    end2 = end - 1 if text[end - 1] in delimiters else end
                    return f"{text[:end - len(pattern2[1])]}{pattern1[1]}{text[end2:]}"
                else:
                    start2 = start + 1 if text[start] in delimiters else start
                    return f"{text[:start2]}{pattern1[0]}{text[start + len(pattern2[0]):]}"
        return None

    def _mixed_pattern_2(self, sent: list) -> Optional[str]:
        text = "".join(map(lambda x: x[0], sent))
        for trigger_words, candidates in random.sample(self.mixed_patterns_2, k=len(self.mixed_patterns_2)):
            for word in trigger_words:
                search = re.search(f"{word}[^{delimiters}]*?[{delimiters}]", text)
                if search is not None:
                    start, end = search.span()
                    candidate = random.choice(candidates)
                    return f"{text[:end - 1]}{candidate}{text[end - 1:]}"
        return None