class Concept:
    def __init__(self, body):
        self.body = body
        self.modifiers = []
        self.prep = ''

    def __str__(self):
        res_str = ''
        for m in self.modifiers:
            res_str = res_str + m + ' '
        res_str = res_str + self.body
        return res_str


class Statement:
    def __init__(self):
        self.left = Concept('')
        self.v = ''
        self.right = Concept('')

    def __str__(self):
        return self.left.__str__() + ' ' + self.v + ' ' + self.right.__str__()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'