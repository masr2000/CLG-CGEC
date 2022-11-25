import re
import random
from typing import Optional

from augmentor import Augmentor

class ImproperCollocation(Augmentor):
    def __init__(self):
        super(ImproperCollocation, self).__init__()
        self.subject_predicate_list = [
            ["目光", "集中", 0, "眼睛"], ["水平", "提高", 1, "改善"], ["条件", "改善", 1, "提高"], ["反响", "热烈", 1, "热情"],
            ["形象", "浮现", 0, "精神"], ["结果", "显示", 1, "显现"], ["成本", "增加", 1, "加强"], ["性别", "平等", 1, "相等"],
            ["基因", "表达", 1, "表现"], ["程度", "严重", 1, "严峻"], ["研究", "表明", 1, "表达"], ["研究", "发现", 1, "发掘"],
            ["技术", "发展", 1, "发现"], ["服务", "周到", 1, "严密"], ["信息", "传递", 1, "递送"], ["病毒", "传播", 1, "传达"]
        ]
        self.predicate_object_list = [
            ["加大", "力度", 0, "加强"], ["提供", "服务", 0, "供应"], ["提高", "效率", 0, "增加"], ["达成", "共识", 0, "完成"],
            ["制定", "政策", 0, "制造"], ["发表", "文章", 0, "发放"], ["采取", "行动", 0, "采纳"], ["实现", "目标", 0, "实施"],
            ["解决", "问题", 0, "决定"], ["传递", "信息", 0, "流传"], ["开展", "活动", 0, "开发"], ["取得", "成就", 0, "开创"],
            ["建立", "模型", 0, "树立"], ["发挥", "作用", 0, "发生"], ["提出", "要求", 0, "提取"], ["创造", "价值", 0, "造成"],
            ["打破", "纪录", 0, "破除"], ["预防", "疾病", 0, "提防"], ["吸取", "教训", 0, "听取"], ["面临", "挑战", 0, "面向"]
        ]
        self.attribute_center_list = [
            ["丰富", "资源", 0, "优裕"], ["重大", "意义", 0, "杰出"], ["宽阔", "", 0, "辽阔"], ["部", "电影", 0, "台"],
            ["性能", "稳定", 1, "安定"], ["密切", "联系", 0, "亲切"], ["热烈", "欢迎", 0, "激烈"], ["慎重", "考虑", 0, "庄重"],
            ["熟练", "掌握", 0, "老练"], ["沉重", "打击", 0, "繁重"], ["幸福", "生活", 0, "幸运"], ["迫切", "需要", 0, "紧迫"],
            ["恶劣", "环境", 0, "劣质"], ["密切", "合作", 0, "亲切"], ["诚信", "经营", 0, "诚实"], ["严厉", "批评", 0, "严格"]
        ]
        self.connective_list = [
            ["无论", "都", 1, "也"], ["只有", "才", 1, "就"], ["尽管", "", 0, "不管"], ["如果", "就", 1, "也"],
            ["不仅", "而且", 1, "但"], ["不仅", "还", 1, "但"], ["宁可", "也", 1, "还"], ["不管", "都", 1, "却"],
            ["虽然", "但", 1, "也"], ["与其", "不如", 1, "也不"], ["要是", "那么", 1, "也"], ["哪怕", "也", 1, "就"]
        ]

    def _replace_subject_predicate(self, sent: list) -> Optional[str]:
        return self.replace_normal_items(sent, self.subject_predicate_list)

    def _replace_predicate_object(self, sent: list) -> Optional[str]:
        return self.replace_normal_items(sent, self.predicate_object_list)

    def _replace_attribute_center(self, sent: list) -> Optional[str]:
        return self.replace_normal_items(sent, self.attribute_center_list)

    def _replace_connective(self, sent: list) -> Optional[str]:
        return self.replace_normal_items(sent, self.connective_list)

    def replace_normal_items(self, sent: list, replace_list: list) -> Optional[str]:
        text = "".join(map(lambda x: x[0], sent))
        for (word1, word2, ridx, rword) in random.sample(replace_list, k=len(replace_list)):
            search = re.search(f"{word1}.*?{word2}", text)
            if search is None:
                continue
            start, end = search.span()
            if ridx == 0:
                return text[:start] + rword + text[start + len(word1):]
            elif ridx == 1:
                return text[:end - len(word2)] + rword + text[end:]
            else:
                raise NotImplementedError
        return None