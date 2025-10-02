def match(pattern, source):
    """Attempt to match pattern to source. % matches a sequence of zero or
        more words and _ matches any single word.

    Args:
        pattern - a list of strings. % and/or _ are utilized as placeholder
                  to match/extract words from the source
        source - a list of string. A phrase/sentence/question represented as
                 a list of words (strings).

    Returns:
        if a match is detected, returns a list of strings - a list of matched
        words (words in the source corresponding to _'s or %'s, in the
        pattern, if any).
        else if no match is detected, returns None. 
    """
    def jn(a, b, c):
        s = ""
        i = b
        while i < c:
            if s == "":
                s = a[i]
            else:
                s = s + " " + a[i]
            i += 1
        return s

    only = True
    k = 0
    while k < len(pattern):
        if pattern[k] == "_" or pattern[k] == "%":
            only = False
            break
        k += 1
    if only:
        if len(pattern) != len(source):
            return None
        i = 0
        while i < len(pattern):
            if pattern[i] != source[i]:
                return None
            i += 1
        return []

    if len(pattern) == 1 and pattern[0] == "%":
        return [jn(source, 0, len(source))]

    hasp = False
    t = 0
    while t < len(pattern):
        if pattern[t] == "%":
            hasp = True
            break
        t += 1
    if not hasp:
        if len(pattern) != len(source):
            return None

    p = 0
    s = 0
    out = []
    sp = -1
    ss = -1
    se = -1
    ci = -1
    ex = False

    def star_last(pp):
        if pp < 0:
            return False
        return pp == len(pattern) - 1

    while s < len(source):
        ex = False
        if p < len(pattern):
            tok = pattern[p]
            if tok != "_" and tok != "%":
                if tok == source[s]:
                    p += 1
                    s += 1
                    continue
                else:
                    ex = False
            elif tok == "_":
                try:
                    out.append(source[s])
                except:
                    return None
                p += 1
                s += 1
                continue
            else:
                sp = p
                ss = s
                se = s
                ci = len(out)
                out.append("")
                p += 1
                continue
        else:
            ex = True

        if sp == -1:
            return None
        if ex and not star_last(sp):
            return None
        if se >= len(source):
            return None
        se += 1
        out[ci] = jn(source, ss, se)
        p = sp + 1
        s = se

    while p < len(pattern) and pattern[p] == "%":
        out.append("")
        p += 1
    if p != len(pattern):
        return None
    return out


assert match(["x", "y", "z"], ["x", "y", "z"]) == [], "test 1 failed"
assert match(["x", "z", "z"], ["x", "y", "z"]) == None, "test 2 failed"
assert match(["x", "y"], ["x", "y", "z"]) == None, "test 3 failed"
assert match(["x", "y", "z", "z"], ["x", "y", "z"]) == None, "test 4 failed"
assert match(["x", "_", "z"], ["x", "y", "z"]) == ["y"], "test 5 failed"
assert match(["x", "_", "_"], ["x", "y", "z"]) == ["y", "z"], "test 6 failed"
assert match(["%"], ["x", "y", "z"]) == ["x y z"], "test 7 failed"
assert match(["x", "%", "z"], ["x", "y", "z"]) == ["y"], "test 8 failed"
assert match(["%", "z"], ["x", "y", "z"]) == ["x y"], "test 9 failed"
assert match(["x", "%", "y"], ["x", "y", "z"]) == None, "test 10 failed"
assert match(["x", "%", "y", "z"], ["x", "y", "z"]) == [""], "test 11 failed"
assert match(["x", "y", "z", "%"], ["x", "y", "z"]) == [""], "test 12 failed"
assert match(["_", "%"], ["x", "y", "z"]) == ["x", "y z"], "test 13 failed"
assert match(["_", "_", "_", "%"], ["x", "y", "z"]) == [
        "x",
        "y",
        "z",
        "",
    ], "test 14 failed"
assert match(["x", "%", "z"], ["x", "y", "z", "z", "z"]) == None, "test 15 failed"
