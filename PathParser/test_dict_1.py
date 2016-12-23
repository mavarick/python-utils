#encoding:utf8

from path_parser_dict import PathParser


def test():
    raw = """
    {
        "rule": "[type:3:type_name][title:2:title_name][season:3:season_name][episode:3:episode_name]",
        "tokens": {
            "type": "电视剧|电影|综艺(节目)?",
            "title": "[\u4e00 -\u9fa5]+",
            "season": "第[一二三四五六七八九十]季",
            "episode": "第([1-9一二三四五六七八九十]|十[一二三四五六七八九]|1[0-9])集",
            "filter": "",
            "replace": "",
            "delimiter": "",
            "unknown": ""
        }
    }
    """
    raw = r"""
        {
            "rule": "[attention:5:attention][unknown:10:][critical:5:critical][unknown:10:][status:5:status]",
            "tokens": {
                "attention": ["(\\d+)\\s*关注", 0],
                "critical": ["(\\d+)\\s*评论", 0],
                "status": "[\u4e00 -\u9fa5]+",
                "filter": "",
                "replace": "",
                "delimiter": "",
                "unknown": "(这里是噪音|这里也是噪音)"
            }
        }
        """

    # \u4e00 -\u9fa5
    # \xe4\xb8\x80-\xe9\xbe\xa5
    pp = PathParser(raw)
    # path_parsers = pp.path_parsers
    s = u"9 关注 这里是噪音 8  评论 这里也是噪音 运营中"
    result = pp.parse(s)
    for k, v in result.iteritems():
        print k, v


def to_utf8(s):
    if isinstance(s, unicode):
        return s.encode("utf8")
    return s


test()