import json
import random
import re

import numpy as np

import json

def seed(i=19260817):
    random.seed(i)
    np.random.seed(i)

if __name__ == "__main__":
    seed()
    methods = [
        # ("redundant_component", "RedundantComponent"),
        # ("missing_component", "MissingComponent"),
        # ("structural_confusion", "StructuralConfusion"),
        # ("improper_logicality", "ImproperLogicality"),
        # ("improper_collocation", "ImproperCollocation"),
        ("improper_word_order", "ImproperWordOrder"),
    ]
    samples = [
        "大连是中国最美丽的城市之一",
        "各种条件的日益成熟强劲地推动了我国叉车行业的快速发展",
        "虽然对这一事件的调查正在进行，但希尔反对做出任何不利于拉扎罗的结论",
        "货物出卖人在交付产品给买受人时，经常提供服务。",
        "本中心之藏书包含台湾文学、语言、历史、文化、政治、族群关系等各领域。",
        "方法利用分组传递拥塞信息，有效地避免了分组的丢失重传。",
        "第三季总的营业费用较上年同期下降18%,为7.75亿美元.",
        "我几乎纯白色，但在夏天，我的皮毛可能会变黄",
        "正是因为民族和艺术风格的多样化，才使今天的国际艺术节如此引人注目",
        "本文主要由三个部分组成：导生制、见习生制、导生制和见习生制的历史作用",
        "春姑娘像一个温柔的妈妈。",
        "在哥伦比亚波哥大美国大使馆门外爆发了激烈的冲突。"
    ]
    for sample in samples:
        print("*" * 30)
        print("Input: ", sample)
        sample = re.sub("\s+", "", sample)
        if sample[-1] not in ['；','！','？',',','!','?','...', "。", "."]:
            sample += "。"
        for _module, _class in methods:
            method = getattr(__import__(_module), _class)()
            output = method.transform(sample)
            print("Output:", json.dumps(output, indent=2, ensure_ascii=False))
