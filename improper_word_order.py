import copy
import random
from typing import Optional

from augmentor import Augmentor

class ImproperWordOrder(Augmentor):
    def __init__(self):
        super(ImproperWordOrder, self).__init__()

    def _reorder_connective(self, sent: list) -> Optional[list]:
        first_connective, first_noun = -1, -1
        for i in range(len(sent)):
            if first_connective != -1 and first_noun != -1:
                break
            if sent[i][1] == "c" and first_connective == -1:
                first_connective = i
            elif sent[i][1].startswith("n") or sent[i][1] == "r" and first_noun == -1:
                first_noun = i
        if first_connective == -1 or first_noun == -1:
            return None
        output = copy.deepcopy(sent)
        # 关联词在主语前
        if first_connective < first_noun:
            noun = output.pop(first_noun)
            output.insert(first_connective, noun)
        # 关联词在主语后
        else:
            connective = output.pop(first_connective)
            output.insert(first_noun, connective)
        return output

    def _reorder_attribute_adverbial(self, sent: list) -> Optional[list]:
        positions = []
        for i in range(1, len(sent)):
            pos1, pos2 = -1, -1
            if i >= len(sent) - 1 or not (sent[i][1] == "v" and sent[i - 1][1] != "u"):
                continue
            else:
                pos1 = i
            j = i + 2 if sent[i + 1][1] == "u" else i + 1
            if j >= len(sent) - 1 or not sent[j][1] == "a":
                continue
            else:
                pos2 = j
            k = j + 2 if sent[j + 1][1] == "u" else j + 1
            if k >= len(sent) - 1 or not (sent[k][1].startswith("n") or sent[k][1] == "v"):
                continue
            positions.append((pos1, pos2))
        if positions:
            pos1, pos2 = random.choice(positions)
            output = copy.deepcopy(sent)
            item = output.pop(pos2)
            if output[pos2][1] == "u":
                output.pop(pos2)
            item[0] = item[0] + "地"
            output.insert(pos1, item)
            return output
        return None

    def _reorder_attribute_center(self, sent: list) -> Optional[list]:
        positions = []
        for i in range(len(sent) - 2):
            # (a/v, u, n) -> (n, u, a/v)
            t0, t1, t2 = sent[i:i + 3]
            if t0[1] in ["a", "v"] and t1[1] == "u" and t2[1].startswith("n"):
                positions.append(i)
        if positions:
            position = random.choice(positions)
            output = copy.deepcopy(sent)
            output[position], output[position + 2] = output[position + 2], output[position]
            return output
        return None