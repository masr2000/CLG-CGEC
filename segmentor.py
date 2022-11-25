from functools import wraps, lru_cache

# n/名词 np/人名 ns/地名 ni/机构名 nz/其它专名
# m/数词 q/量词 mq/数量词 t/时间词 f/方位词 s/处所词
# v/动词 a/形容词 d/副词 h/前接成分 k/后接成分
# i/习语 j/简称 r/代词 c/连词 p/介词 u/助词 y/语气助词
# e/叹词 o/拟声词 g/语素 w/标点 x/其它
segmentor = None

@lru_cache(maxsize=1000)
def word_seg(sent):
    global segmentor
    if segmentor is None:
        import thulac
        segmentor = thulac.thulac()
    return segmentor.cut(sent)

def seg_dec(func):
    @wraps(func)
    def _func(obj, sent, *args, **kwargs):
        if isinstance(sent, str):
            original_sent = sent
            sent = word_seg(sent)
        else:
            original_sent = "".join(map(lambda x: x[0], sent))
        result, rules = func(obj, sent, *args, **kwargs)
        for i in range(len(result)):
            if isinstance(result[i], list):
                # ["xxx", "yyy", ...]
                if isinstance(result[i][0], str):
                    result[i] = "".join(result[i])
                # [["xxx", "n"], ["yyy", "v"], ...]
                elif isinstance(result[i][0], list):
                    result[i] = "".join(map(lambda x: x[0], result[i]))
                # else: "xxxyyy..."
        return {"type": obj.__class__.__name__, "origin": original_sent, "transform": result, "rules": rules}
    return _func