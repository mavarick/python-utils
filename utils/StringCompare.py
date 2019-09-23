#encoding:utf8


class StringCompare(object):
    def LCS(self, s1, s2):
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
        return ''.join(s)

    def lcs_len(self, s1, s2):
        s1, s2 = self.to_unicode(s1), self.to_unicode(s2)
        m = [[0 for x in range(len(s2) + 1)] for y in range(len(s1) + 1)]
        for p1 in range(len(s1)):
            for p2 in range(len(s2)):
                if s1[p1] == s2[p2]:
                    m[p1 + 1][p2 + 1] = m[p1][p2] + 1
                elif m[p1 + 1][p2] > m[p1][p2 + 1]:
                    m[p1 + 1][p2 + 1] = m[p1 + 1][p2]
                else:
                    m[p1 + 1][p2 + 1] = m[p1][p2 + 1]
        return m[len(s1)][len(s2)]



    def to_unicode(self, s):
        if not isinstance(s, unicode):
            return s.decode("utf8")
        return s

    def to_utf8(self, s):
        if isinstance(s, unicode):
            return s.encode("utf8")
        return s


class ListCompare(object):

    @staticmethod
    def LCS(s1, s2):
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
        return s

    @staticmethod
    def CS(array1, array2):
        """
        Common String, 找出两个字符串中的重叠部分

        Parameters::
            filter: if True, 只是对比其中的汉字和英文字符
        Return::
            两个的公共字符创
        """
        common = []
        for item in array1:
            if item in array2:
                common.append(item)
        return common


class CS(object):
    def evaluate(self, s1, s2):
        s1, s2 = self.to_unicode(s1), self.to_unicode(s2)
        common = []
        for item in s1:
            if item in s2:
                common.append(item)
        s = map(self.to_utf8, common)
        return ''.join(s)

    def to_unicode(self, s):
        if not isinstance(s, unicode):
            return s.decode("utf8")
        return s

    def to_utf8(self, s):
        if isinstance(s, unicode):
            return s.encode("utf8")
        return s


def test():
    s1, s2 = "abcdefgh", "adcfegh"
    s1 = u"1979年10月28日星期天晴"
    s2 = u"1979年10月28日 阳光灿烂的星期天"
    # print StringCompare.LCS(s1, s2)

    cs = CS()
    print cs.evaluate(s1, s2)


if __name__ == "__main__":
    test()
