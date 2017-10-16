import re
import math


def tryParseNumber(value):
    if (isinstance(value, bool)):
        return 1 if value else 0
    # reg = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
    # result = reg.match(value)
    if (isinstance(value, str)):
        return value
    else:
        if (value - math.floor(value)):
            return value
        else:
            return math.floor(value)


class TypeChecker(object):
    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def javaType(self):
        return self._javaType

    @javaType.setter
    def javaType(self, value):
        self._javaType = value

    @property
    def idx(self):
        return self._idx

    @idx.setter
    def idx(self, value):
        self._idx = value

    def check(self, value):
        pass


# 处理 any 类型的数据
class AnyChecker(TypeChecker):
    @property
    def type(self):
        return "any"

    @property
    def javaType(self):
        return "String"

    @property
    def idx(self):
        return 0

    def check(self, value):
        return tryParseNumber(value)


# 处理 string 类型的数据
class StringChecker(TypeChecker):
    @property
    def type(self):
        return "string"

    @property
    def javaType(self):
        return "String"

    @property
    def idx(self):
        return 1

    def check(self, value):
        return value


# 处理 number 类型的数据
class NumberChekcer(TypeChecker):
    @property
    def type(self):
        return "number"

    @property
    def javaType(self):
        return "double"

    @property
    def idx(self):
        return 2

    def check(self, value):
        if (value == ""): return 0
        if(isinstance(value,str)):
            value = float(value)
        if (value - math.floor(value)):
            return value
        else:
            return math.floor(value)


# 处理 boolean 类型的数据
class BooleanChecker(TypeChecker):
    @property
    def type(self):
        return "boolean"

    @property
    def javaType(self):
        return "bool"

    @property
    def idx(self):
        return 3

    def check(self, value):
        if (value == ""): return 0
        if (value.low() == "false"):
            return 0
        else:
            return 1


# 处理 | 类型的数据
class ArrayCheker(TypeChecker):
    @property
    def type(self):
        return "any[]"

    @property
    def javaType(self):
        return "Object[]"

    @property
    def idx(self):
        return 4

    def check(self, value):
        tmp = value.split(":")
        arr = []
        for v in tmp:
            arr.append(tryParseNumber(v));
        return arr


# 处理 |: 类型的二维数组的数据
class Array2DCheker(TypeChecker):
    @property
    def type(self):
        return "any[][]"

    @property
    def javaType(self):
        return "Object[][]"

    @property
    def idx(self):
        return 5

    def check(self, value):
        arr = []
        tmp = value.split("|")
        for v in tmp:
            tmp2 = v.split(":")
            arr2 = []
            for v2 in tmp2:
                arr2.append(tryParseNumber(v));
            arr.append(arr2)
        return arr


# 日期检查器 yyyy-MM-dd
class DateChecker(TypeChecker):
    @property
    def type(self):
        return "Date"

    @property
    def javaType(self):
        return "String"

    @property
    def idx(self):
        return 6

    def check(self, value):
        pass


checkers = {}
checkers[""] = AnyChecker()
checkers["number"] = NumberChekcer()
checkers["string"] = StringChecker()
checkers["boolean"] = BooleanChecker()
checkers[":"] = ArrayCheker()
checkers["|:"] = Array2DCheker()
# print(checkers["|:"].check("1s2333:123:333|sdsd:23"))
