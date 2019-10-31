from fractions import Fraction
import gzip
import requests
import sys

def convergents(seq):
    assert len(seq) > 0, 'got empty sequence'
    prev = (1, 0)
    curr = (seq[0], 1)
    yield curr
    for n in seq[1:]:
        next = (n*curr[0] + prev[0], n*curr[1] + prev[1])
        prev = curr
        curr = next
        yield curr

def get_seq(id):
    assert 0 <= id and id < 1000000, f'invalid id {id}'
    url = f'https://oeis.org/search?q=id:A{id:06}&fmt=json'
    response = requests.get(url)
    return response.json()['results'][0]

def pair2rat(numerator, denominator):
    if numerator < 0 and denominator < 0:
        return '{}/{}'.format(-numerator, -denominator)
    elif numerator < 0 or denominator < 0:
        return '-{}/{}'.format(abs(numerator), abs(denominator))
    else:
        return '{}/{}'.format(numerator, denominator)
        

def pair2float(numerator, denominator):
    if denominator == 0:
        return float('NaN')
    else:
        return numerator / denominator

def show_seq(id):
    seq = get_seq(id)
    if seq is None:
        return
    print(seq['name'])
    integers = [int(n) for n in seq['data'].split(',')]
    full = 'full' in seq['keyword'].split(',')
    print('[{}; {}{}]'.format(
        integers[0],
        ', '.join(map(str, integers[1:])),
        '' if full else ', ...'
    ))
    cs = list(convergents(integers))
    print([pair2rat(x[0], x[1]) for x in cs])
    print([pair2float(x[0], x[1]) for x in cs])

def get_all_convergents(fname):
    cs = [None]
    n = 1
    with gzip.open(fname, 'rt') as fin:
        for line in fin:
            if line.startswith('#'):
                continue
            seq = line.split(',')
            idx = int(seq[0][1:])
            while n < idx:
                cs.append(None)
                n += 1
            numbers = [int(x) for x in seq[1:-1]]
            for c in convergents(numbers):
                pass # ignore all but the last convergent
            cs.append(c)
            n += 1
    return cs
            
def show_all_convergents(fname):
    cs = get_all_convergents(fname)
    for (i, c) in enumerate(cs):
        if c is None:
            continue
        print('A{:06} {} {}'.format(i, pair2rat(c[0], c[1]), pair2float(c[0], c[1])))

def main():
    if len(sys.argv) > 1:
        show_seq(int(sys.argv[1]))
    else:
        # assumes https://oeis.org/stripped.gz is in the current directory
        show_all_convergents('stripped.gz')

if __name__ == '__main__':
    main()

