# CLG-CGEC

*Pytorch Implementation for EMNLP2022 Findings (Long Paper)*

*"Linguistic Rules-Based Corpus Generation for Native Chinese Grammatical Error Correction".*

## 概述

本论文的主要贡献包括如下两部分：

1. 提出了基于中文语法规则的CGEC数据生成方法CLG，该方法可以依据不同类型语法错误的语法规则将语法正确的句子转化为含有不同类型错误的句子。
2. 构建了一个具有挑战性的CGEC评测数据集NaCGEC，该数据集的语料来源于中文母语者，更接近中文母语者日常写作中会犯的语法错误。

**本仓库包含了我们提出的CGEC数据生成方法CLG的代码实现，而本文构建的测试数据集NaCGEC预期将于近期依托学术会议举办相关比赛，因此测试数据将在比赛时放出。**

另外，论文实验中使用的CGEC模型实现请参考[MuCGEC](https://github.com/HillZhang1999/MuCGEC)。

## 实验环境

- Python >= 3.8
- thulac ~= 0.2.1
- synonyms ~= 3.16.0

## 使用说明

代码实现中包含生成含有六类不同语法错误的方法，这六类语法错误以及其对应的生成规则所在类包括：

- 成分残缺：`missing_component.MissingComponent`
- 成分赘余：`redundant_component.RedundantComponent`
- 搭配不当：`improper_collocation.ImproperCollocation`
- 不合逻辑：`improper_logicality.ImproperLogicality`
- 语序不当：`improper_word_order.ImproperWordOrder`
- 句式杂糅：`structural_confusion.StructuralConfusion`

这六个类均继承自`Augmentor`类，使用统一的`transform`接口来将正确的句子转化为含有不同语法错误的句子。一个简单的使用示例：

```python
import json
from improper_word_order import ImproperWordOrder
method = ImproperWordOrder()
sample = "春姑娘像一个温柔的妈妈。"
output = method.transform(sample)
print(json.dumps(output, ensure_ascii=False, indent=2))
```

预期输出如下：

```json
{
  "type": "ImproperWordOrder",
  "origin": "春姑娘像一个温柔的妈妈。",
  "transform": [
    "春姑娘像一个妈妈的温柔。"
  ],
  "rules": [
    "_reorder_attribute_center"
  ]
}
```

更多的示例参见`main.py`。

使用这六个类即可自动化地实现CGEC任务的数据增强，批量生成含有语法错误的样本。该方法可以与现有方法和数据集兼容，即可以使用该方法生成的训练数据与其他数据增强方法生成的数据或其他训练数据联合使用进行模型训练。

## 联系我们

本项目代码在后期开源整理的过程中为了可读性和可用性，对代码逻辑和结构进行了大量的调整，因此实验效果可能与论文中使用的最初版本有一定差别，后续还会进一步对相关规则进行完善。

如果您对我们的工作有任何问题，请联系masr21@mails.tsinghua.edu.cn或liyinghu20@mails.tsinghua.edu.cn。

如果您认为我们的工作有帮助，可以引用我们的论文：

```
@inproceedings{ma2022linguistic,
  title={Linguistic Rules-Based Corpus Generation for Native Chinese Grammatical Error Correction},
  author={Ma, Shirong and Li, Yinghui and Sun, Rongyi and Zhou, Qingyu and Huang, Shulin and Zhang, Ding and Yangning, Li and Liu, Ruiyang and Li, Zhongli and Cao, Yunbo and others},
  booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2022},
  year={2022}
}
```

