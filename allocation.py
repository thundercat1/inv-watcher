from __future__ import print_function

import operator


def allocate(percents, total):
    #percents = {'S': .25, 'M': .25, 'L': .5}
    #allocate(percents, 100) --> {'S': 25, 'M': .25, 'L': .5}
    res = {size: None if percents[size] is None else 0 for size in percents}
    remaining = total
    allotted = 0

    current_percents = {size: None if percents[size] is None else 0 for size in percents}
    while remaining > 0:
        current_error = {size: current_percents[size]-percents[size] if percents[size] is not None else 0 for size in percents}
        shortest_size = sorted(current_error.items(), key=operator.itemgetter(1))[0][0]
        res[shortest_size] += 1
        allotted += 1
        remaining -= 1

        current_percents = {size: None if res[size] is None else float(res[size])/allotted for size in res}

    return res

