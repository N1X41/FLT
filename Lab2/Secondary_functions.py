def rewrite(line, rules):
    ended = False
    while not ended:
        ended = True
        for i in range(len(line)):
            for j in range(1, rules[0] + 1):
                for k in rules[1:len(rules)]:
                    if line[i:i+j] == k[0]:
                        line = line[0:i] + k[1] + line[i+j:len(line)]
                        ended = False
    return line


def read():
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        lines.append(line)
    return lines
