"""Exact checker for KG(10,5,3). Requires Python >=3.10 and a C++20 compiler."""
from collections import Counter
from itertools import combinations
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import os
import subprocess


def layer(n, k):
    return [sum(1 << i for i in s) for s in combinations(range(n), k)]


def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def maximal_cliques(neighbors, chosen, possible, excluded):
    if not (possible | excluded):
        yield chosen
        return
    pivot = max(bits(possible | excluded), key=lambda i: (possible & neighbors[i]).bit_count())
    for i in bits(possible & ~neighbors[pivot]):
        yield from maximal_cliques(neighbors, chosen | 1 << i,
                                   possible & neighbors[i], excluded & neighbors[i])
        possible ^= 1 << i
        excluded |= 1 << i


def relabelings(seeds, vertices):
    """Close anchored families under adjacent transpositions, generators of S_10."""
    index = {v: i for i, v in enumerate(vertices)}
    transpositions = []
    for point in range(9):
        shifts = {}
        for i, v in enumerate(vertices):
            w = v ^ (3 << point) if (v >> point) & 3 in (1, 2) else v
            offset = index[w] - i
            shifts[offset] = shifts.get(offset, 0) | 1 << i
        transpositions.append(tuple(shifts.items()))
    queue = list(seeds)
    seen = set(queue)
    for family in queue:
        for perm in transpositions:
            image = sum((family & mask) << off if off >= 0 else (family & mask) >> -off
                        for off, mask in perm)
            if image not in seen:
                queue.append(image)
                seen.add(image)
    return sorted(seen)


def cover_proof(columns):
    source = Path(__file__).with_name('cover.cpp')
    compiler = os.environ.get('CXX', 'c++')
    word = (1 << 64) - 1
    payload = ''.join(f'{h} ' + ' '.join(f'{(v >> i) & word:x}' for i in range(0, 256, 64)) + '\n'
                      for h, v in columns)
    with TemporaryDirectory() as tmp:
        exe = Path(tmp) / 'cover'
        subprocess.run([compiler, '-std=c++20', '-O3', str(source), '-o', str(exe)], check=True)
        proof = json.loads(subprocess.run([str(exe)], input=payload, capture_output=True,
                                          text=True, check=True).stdout)
    proof['cover_source_sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
    proof['input_sha256'] = hashlib.sha256(payload.encode()).hexdigest()
    proof['compiler'] = subprocess.check_output([compiler, '--version'], text=True).splitlines()[0]
    return proof


def rounding_check():
    """Exhaust finite tie cases from SIX-LISTS.md, using twice the half-integral target."""
    cases = ((6, ((3, 3),)), (7, ((2, 1), (2, 2), (3, 2), (3, 3))))
    worst = {}
    for n, rows in cases:
        triples = layer(n, 3)
        worst[n] = max(sum(abs(2 * (y & h).bit_count() - twice) >= 3 for y in triples)
                       for size, twice in rows for h in layer(n, size))
        if 6 * worst[n] >= len(triples):
            raise ValueError('six constraints may exhaust the rounding choices')
    return worst


def check():
    vertices = layer(10, 5)
    all_points = (1 << 10) - 1
    full = (1 << len(vertices)) - 1
    supports = layer(10, 3) + vertices + layer(10, 7)
    families = [sum(1 << i for i, v in enumerate(vertices)
                    if 2 * (v & h).bit_count() >= h.bit_count() + 3) for h in supports]
    compatible = [sum(1 << j for j, b in enumerate(vertices) if b != a and (a & b).bit_count() >= 3)
                  for a in vertices]
    # Any family with no pair meeting in exactly three lies among a fixed vertex
    # and its one-swap neighbors; the swaps form a pairwise incident edge family
    # of K_{5,5}, hence a star (<=5 swaps). Otherwise relabel the distance-two pair.
    a = 0
    b = next(i for i, v in enumerate(vertices) if (v & vertices[a]).bit_count() == 3)
    hist = Counter()
    seeds = []
    for f in maximal_cliques(compatible, 1 << a | 1 << b, compatible[a] & compatible[b], 0):
        hist[f.bit_count()] += 1
        if f.bit_count() > 14 and not any(f & ~h == 0 for h in families):
            seeds.append(f)
    extra = relabelings(seeds, vertices)
    result = cover_proof(list(zip(supports, families)) + [(-1, f) for f in extra])
    # Replay the known upper bound rather than treating fourteen as a search result.
    lines = [sum(1 << (p - 1) for p in (i, j, i ^ j))
             for i in range(1, 8) for j in range(i + 1, 8) if j < (i ^ j)]
    fano = [v for h, v in zip(supports, families) if h in lines or (all_points ^ h) in lines]
    covered = 0
    for f in fano:
        for i in bits(f):
            if f & ~(compatible[i] | 1 << i):
                raise ValueError('non-independent Fano class')
        covered |= f
    if len(fano) != 14 or covered != full:
        raise ValueError('incomplete Fano cover')
    return {'vertices': len(vertices), 'anchored_maximal_families_by_size': dict(sorted(hist.items())),
            'omitted_size_upper_bound': 14, 'structured_classes': len(families),
            'other_large_classes': len(extra), 'cover_proof': result, 'fano_cover_size': len(fano),
            'six_list_max_bad_choices_per_row': rounding_check()}


if __name__ == '__main__':
    print(json.dumps(check(), sort_keys=True))
