import random
import re
from typing import Union, Optional

from augmentor import Augmentor

DEBUG = False

class MissingComponent(Augmentor):
    def __init__(self):
        super(MissingComponent, self).__init__()
        self.connective_list = [('不但', '还'), ('不但', '也'), ('不光', '还'), ('不仅', '而且'),
            ('不仅', '还'), ('不只', '又'),  ('不但', '并且'), ('不但', '而且'),
            ('别说', '就'), ('不单', '还'), ('不但', '反而'), ('不但', '更'),
            ('不但', '相反'), ('不光', '而且'), ('不光', '就是'), ('不光', '也'),
            ('不仅', '反而'), ('不仅', '就是'), ('不仅', '甚至'), ('不仅', '也'),
            ('不仅', '尤其'), ('不只', '还'), ('非但', '反而'), ('由于', '因此'),
            ('因为', '才'), ('因为', '便'), ('因为', '就'), ('因为', '以致'),
            ('由于', '所以'), ('即使', '也'), ('假如', '就'), ('就是', '也'),
            ('就算', '也'), ('如果', '就'), ('如果', '那么'), ('就算', '总'),
            ('既是', '也'), ('即使', '还'), ('即使', '总'), ('哪怕', '都'),
            ('倘若', '便'), ('若是', '则'), ('若是', '那'), ('若是', '就'),
            ('尽管', '可'), ('尽管', '却'), ('虽然', '可是'), ('虽然', '却'),
            ('虽然', '但'), ('虽说', '但'), ('固然', '不过'), ('固然', '但'),
            ('尽管', '也'), ('虽然', '可'), ('虽然', '然而'), ('虽说', '也'),
            ('幸而', '否则'), ('虽则', '也'), ('幸亏', '不然'), ('虽然', '还'),
            ('假使', '还'), ('要是', '那么'), ('只要', '就'), ('只有', '才'),
            ('无论', '都'), ('不管', '也'), ('因为', '所以'), ('既然', '那么'),
            ('既然', '就'), ('之所以', '是因为'), ('不是', '而是'), ('不是', '就是'),
            ('既', '又'), ('一', '就'), ('与其', '不如'), ('宁可', '也不')]
        self.verb_list = list(
            {'过着', '取得', '获得', '参加', '开展', '举办', '承担', '缺乏', '改善', '培养', '具备', '拥有', '打破',
             '打碎', '破坏', '修复', '维护', '修护', '承办', '害怕', '爱', '骂', '收拾', '推翻', '充满', '剔除', '去除',
             '取出', '祛除', '驱除', '赶出', '拿出', '袒护', '弹奏', '打开', '关闭', '欣赏', '挥舞', '挥动', '甩', '拧',
             '痛恨', '铭记', '牢记', '找', '招收', '招揽', '合上', '操作', '使用', '编辑', '手持', '批评', '宣传',
             '保卫', '研究', '打听', '聆听', '探望', '缅怀', '鄙视', '蔑视', '歧视', '打量', '遥望', '看护', '保护',
             '搀', '抱', '搂', '扶', '捉', '擒', '掐', '推', '拿', '抽', '撕', '摘', '拣', '捡', '打', '播', '击', '捏',
             '撒', '按', '弹', '撞', '提', '扭', '捶', '持', '揍', '披', '捣', '搜', '托', '举', '拖', '擦', '敲', '挖',
             '抛', '掘', '抬', '插', '扔', '写', '抄', '摇', '抓', '捧', '掷', '撑', '摊', '倒', '摔', '劈', '画', '搔',
             '撬', '挥', '揽', '挡', '捺', '抚', '搡', '拉', '摸', '拍', '剪', '拎', '拔', '拨', '舞', '握', '攥', '咬',
             '吞', '吐', '吮', '吸', '啃', '喝', '吃', '咀', '嚼', '瞥', '视', '盯', '瞧', '窥', '瞄', '眺', '瞪',
             '瞅'})
        self.attribute_list = [
            ('相当', ['a']), ('非常', ['a']), ('很', ['a']), ('极其', ['a']), ('十分', ['a']),
            ('极', ['a']), ('最', ['a']), ('顶', ['a']), ('太', ['a']), ('更', ['a']),
            ('挺', ['a']), ('格外', ['a']), ('分外', ['a']), ('更加', ['a']), ('越', ['a']),
            ('越发', ['a']), ('有点', ['a']), ('有点儿', ['a']), ('稍', ['a']), ('稍微', ['a']),
            ('稍稍', ['a']), ('略微', ['a']), ('略', ['a']), ('几乎', ['a']), ('过于', ['a']),
            ('尤其', ['a']), ('特别', ['a']), ('真', ['a']), ('真是', ['a'])
        ]
        self.adverbial_list = [
            ('分别', ['v']), ('各自', ['v']), ('各', ['v']), ('情愿', ['v']),
            ('肯', ['v']), ('要', ['v']), ('愿', ['v']), ('想要', ['v']),
            ('要想', ['v']), ('敢', ['v']), ('敢于', ['v']), ('乐于', ['v']), ('应', ['v']),
            ('应当', ['v']), ('得', ['v']), ('该', ['v']), ('当', ['v']), ('须得', ['v']),
            ('理当', ['v']), ('便于', ['v']), ('难于', ['v']), ('难以', ['v']), ('易于', ['v']),
        ]
        self.complement_list = [
            ('考虑', '一下'), ('思考', '一下'), ('想', '一下'), ('打了', '一下'), ('丢', '不得'),
            ('去', '不得'), ('大意', '不得'), ('耽误', '不得'), ('建设', '得'), ('建设', '成'),
        ]

    def _missing_connective(self, sent: list) -> Optional[str]:
        text = "".join(map(lambda x: x[0], sent))
        for (word1, word2) in random.sample(self.connective_list, k=len(self.connective_list)):
            search = re.search(f"{word1}.+?{word2}", text)
            if search is not None:
                start, end = search.span()
                return text[:end - len(word2)] + text[end:]
        return None

    def _missing_subjective(self, sent: list) -> Optional[list]:
        candidates = ["使", "使得", "令", "让"]
        for i in range(1, len(sent) - 2):
            if sent[i][0] == "，" and sent[i + 1][1] in ["np", "r"]:
                candidate = random.choice(candidates)
                return [*sent[:i + 1], [candidate, "v"], *sent[i + 1:]]
        return None

    def _missing_predicate_1(self, sent: list) -> Optional[list]:
        remove_list = []
        for i in range(1, len(sent) - 1):
            if sent[i][1] == "v" and sent[i][0] in self.verb_list:
                for j in range(i + 1, len(sent)):
                    if sent[j][1] in ["w", "x"]:
                        break
                    if sent[j][1] in ["n"]:
                        remove_list.append(i)
        if remove_list:
            ri = random.choice(remove_list)
            return sent[:ri] + sent[ri + 1:]
        return None

    def _missing_predicate_2(self, sent: list) -> Optional[list]:
        for i in range(len(sent)):
            if sent[i][1] == "v" and sent[i][0] in self.verb_list:
                return [*sent[:i], ["为", "p"], *sent[i + 1:]]
        return None

    def _missing_objective(self, sent: list) -> Optional[list]:
        remove_list = []
        for i in range(1, len(sent)):
            if sent[i][1] in ["n", "np", "r"] and sent[i - 1][1] == "v":
                remove_list.append(i)
        if remove_list:
            ri = random.choice(remove_list)
            return sent[:ri] + sent[ri + 1:]
        return None

    def _missing_attribute(self, sent: list) -> Optional[list]:
        word_list = list(map(lambda x: x[0], sent))
        for (word, pos) in random.sample(self.attribute_list, k=len(self.attribute_list)):
            if word not in word_list:
                continue
            for i in range(1, len(sent)):
                if sent[i - 1][0] == word and sent[i][1] in pos:
                    return sent[:i] + sent[i + 1:]
        return None

    def _missing_adverbial(self, sent: list) -> Optional[list]:
        word_list = list(map(lambda x: x[0], sent))
        for (word, pos) in random.sample(self.attribute_list, k=len(self.attribute_list)):
            if word not in word_list:
                continue
            for i in range(1, len(sent)):
                if sent[i - 1][0] == word and sent[i][1] in pos:
                    return sent[:i - 1] + sent[i:]
        return None

    def _missing_complement(self, sent: list) -> Optional[str]:
        text = "".join(map(lambda x: x[0], sent))
        for (word1, word2) in self.complement_list:
            word = word1 + word2
            if word in text:
                return text.replace(word, word1)
        return None
