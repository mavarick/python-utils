#encoding:utf8

OFFSET = 0.01


class LCS(object):
    def evaluate(self, s1, s2):
        if not s1 or not s2:
            return ""
        s1, s2 = self.to_unicode(s1), self.to_unicode(s2)
        # 生成字符串长度加1的0矩阵，m用来保存对应位置匹配的结果
        m = [[0 for x in range(len(s2) + 1)] for y in range(len(s1) + 1)]
        # d用来记录转移方向
        d = [[None for x in range(len(s2) + 1)] for y in range(len(s1) + 1)]

        for p1 in range(len(s1)):
            for p2 in range(len(s2)):
                if s1[p1] == s2[p2]:  # 字符匹配成功，则该位置的值为左上方的值加1
                    m[p1 + 1][p2 + 1] = m[p1][p2] + 1
                    d[p1 + 1][p2 + 1] = 'ok'
                elif m[p1 + 1][p2] > m[p1][p2 + 1]:  # 左值大于上值，则该位置的值为左值，并标记回溯时的方向
                    m[p1 + 1][p2 + 1] = m[p1 + 1][p2]
                    d[p1 + 1][p2 + 1] = 'left'
                else:  # 上值大于左值，则该位置的值为上值，并标记方向up
                    m[p1 + 1][p2 + 1] = m[p1][p2 + 1]
                    d[p1 + 1][p2 + 1] = 'up'
        (p1, p2) = (len(s1), len(s2))
        # print numpy.array(d)
        s = []
        while m[p1][p2]:  # 不为None时
            c = d[p1][p2]
            if c == 'ok':  # 匹配成功，插入该字符，并向左上角找下一个
                s.append(s1[p1 - 1])
                p1 -= 1
                p2 -= 1
            if c == 'left':  # 根据标记，向左找下一个
                p2 -= 1
            if c == 'up':  # 根据标记，向上找下一个
                p1 -= 1
        s.reverse()
        s = map(self.to_utf8, s)

        min_ratio = (len(s) * 1.0 + OFFSET) / (min(len(s1), len(s2)) + OFFSET)
        max_ratio = (len(s) * 1.0 + OFFSET) / (max(len(s1), len(s2)) + OFFSET)
        v = ''.join(s)
        return "v:%s;r1:%s;r2:%s"%(v, min_ratio, max_ratio)

    def to_unicode(self, s):
        if not isinstance(s, unicode):
            try:
                return s.decode("utf8")
            except:
                return s
        return s

    def to_utf8(self, s):
        if isinstance(s, unicode):
            try:
                return s.encode("utf8")
            except:
                return s
        return s