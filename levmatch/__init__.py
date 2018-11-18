import re
from fuzzywuzzy.fuzz import ratio
from fuzzywuzzy.StringMatcher import StringMatcher


class ProcessedLog:
    def __init__ (self, string):
        self.line = string
        self.num = 1
        self.colored_line = string

    def try_merge(self, line, color):
        if ratio(self.line, line) > 80:
            self.num += 1
            if self.num == 2 and color:
                self.set_color(line)
            return True
        return False

    def set_color(self, line):
        diffstring = ""
        sm = StringMatcher(seq1=self.line, seq2=line)
        mb = sm.get_matching_blocks()
        i = 0
        for block in mb:
            diffstring += "\x1b[33m%s\x1b[0m" % self.line[i:block[0]]
            diffstring += self.line[block[0]:block[0] + block[2]]
            i = block[0] + block[2]
        self.colored_line = diffstring


def merge_plogs(processed_logs, line, color):
    for plog in processed_logs:
        if plog.try_merge(line, color):
            return True
    return False


def parse_log(stream, color):
    processed_logs = []
    for line in stream.readlines():
        line = re.sub('[0-9]{2}:[0-9]{2}:[0-9]{2}', '', line)
        if not merge_plogs(processed_logs, line, color):
            processed_logs.append(ProcessedLog(line))
    processed_logs.sort(key=lambda x: -x.num)
    l_pad = len(str(max([log.num for log in processed_logs])))
    str_fmt = "%0{0}d %s".format(l_pad) if not color else "\x1b[31m%0{0}d\x1b[0m %s".format(l_pad)
    print_lines = [str_fmt % (log.num, log.colored_line) for log in processed_logs]
    return print_lines


def match(stream, matchline):
    processed_logs_lst = []
    for line in stream.readlines():
        line_strip = re.sub('[0-9]{2}:[0-9]{2}:[0-9]{2}', '', line)
        if ratio(matchline, line_strip) > 80:
            processed_logs_lst.append(line)
    return processed_logs_lst

