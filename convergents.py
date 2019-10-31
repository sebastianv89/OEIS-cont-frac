from fractions import Fraction
import requests
import sys

def convergents(seq):
    if len(seq) == 0:
        return
    prev = Fraction(seq[0], 1)
    yield prev
    if len(seq) == 1:
        return
    curr = Fraction(seq[0]*seq[1] + 1, seq[1])
    yield curr
    for n in seq[2:]:
        next = Fraction(
            n*curr.numerator + prev.numerator,
            n*curr.denominator + prev.denominator
        )
        prev = curr
        curr = next
        yield curr
        

def get_seq(id):
    assert 0 <= id and id < 1000000, f'invalid id {id}'
    url = f'https://oeis.org/search?q=id:A{id:06}&fmt=json'
    response = requests.get(url)
    return response.json()['results'][0]

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
    print(['{}/{}'.format(x.numerator, x.denominator) for x in cs])
    print([float(x) for x in cs])

def main():
    show_seq(int(sys.argv[1]))

if __name__ == '__main__':
    main()
