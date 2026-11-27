# A06 — Can ten people always divide goods fairly between two fixed groups?

**Open for arbitrary preferences and arbitrary numbers of goods. Yes for up to ten goods, even with twelve people.** Alipour and Jafari guarantee nine people any number of goods. Our finite result narrows the chromatic number for ten goods from the cited interval [10,14] to **[13,14]**. This is an exact finite computation, independently reproduced in-session, **unrefereed**. It is not a claim to have determined the exact threshold or priority.

Two further written results apply to **any number of goods**:

- [Ten people suffice if each person's valuation depends on at most four goods](FOUR-GOOD-SUPPORT.md). The four can differ for each person and the valuations need not be additive.
- [Six approval lists can all be balanced to within two](SIX-LISTS.md). Any number of people whose preferences depend monotonically on counts on those lists are covered. Even one additional unrestricted person can choose the orientation. Seven lists can fail simultaneous balance; that is not a ten-person impossibility.

**Fairness here** means each person weakly prefers their group's bundle after removing at most two goods of their choice from the comparison bundle. The goods are shared within two prescribed nonempty groups, not divided into ten individual shares. The bundles must differ in size by at most one. See [sources and definitions](SOURCES.md).

## Why the finite result proves fairness

On 2k goods, represent an allocation by the k goods given to the first group. Join two allocations when their sets share at most two goods. A single agent cannot reject two adjacent allocations: deleting the at most two goods outside both sets from the comparison bundle shows that rejection at A forces u(A)<u(B), while rejection at B forces the reverse. For a second-group agent, take complements. So failure for twelve agents would cover the graph by twelve independent sets, one per rejecting agent. Conversely every independent set can be realized as a rejection family by a monotone binary valuation ([Alipour–Jafari, Theorem 2.1](https://arxiv.org/html/2611.04486v1#S2.Thmtheorem1)). The threshold is strict: thirteen colors needed guarantees twelve people, not thirteen.

For ten goods our checker rules out every twelve-class cover, not merely covers by specially shaped families. It also verifies the known fourteen-class Fano cover. Therefore twelve people are guaranteed, fourteen can fail, and thirteen are undecided **on ten goods**. An irrelevant dummy transfers existence to nine. On eight goods the cited paper gives exactly fourteen colors, on six the graph is complete on twenty vertices, and at most four goods any balanced comparison bundle can be deleted. Together with the odd-size reduction this yields the stated guarantee for all goods counts up to ten. For all goods counts combined the known agent interval is still [9,13].

## Exact finite proof

1. **Classify large families.** Independent classes consist of five-sets that meet pairwise in at least three places. If there is no pair meeting in exactly three, fix one member. Every other member differs from it by one swap. Any two such swaps must share an endpoint. In a bipartite graph these swaps form a star, so there are at most five, besides the fixed member. Otherwise relabel a pair meeting in three as 12345 and 12367. A pivoted maximal-clique enumeration on their 70 common compatible neighbors classifies *all* maximal extensions of this pair. The seven sizes and their multiplicities are in the [receipt](RECEIPT.json).
2. **Restore all labels.** For each support H of size 3, 5 or 7, use the family of five-sets containing at least (|H|+3)/2 points of H. These are respectively triple stars, radius-one balls and complements of triple stars. For anchored maximal families larger than 14 not contained in one of those, apply adjacent coordinate transpositions to closure. This yields 33,600 exceptions, each of size 18, in addition to the 492 structured families. Every independent class either has size at most 14 or can be enlarged into a listed family. A coloring can be tested as a cover since overlaps can always be assigned to one of their covering classes.
3. **Exclude twelve classes.** With N vertices still uncovered and q slots left, some remaining class must cover at least ceil(N/q) of them. The search stops with an error, not a proof, if this demand ever reaches 14 or less. The maximum possible total marginal contribution from q classes is also bounded by the sum of their q greatest individual gains, padding with demand−1 for classes below demand. A subproblem is impossible if this sum is too small. Overcounting intersections only makes the bound more generous.
4. **Enumerate symmetry without losing choices.** Previous structured supports partition the ten goods into cells having the same membership history. Permutations within each cell preserve the residual problem. Two new supports are equivalent exactly when they take the same number of goods from each cell. At each node order the groups by (gain, orbit key), and branch on the **highest group used** in a hypothetical cover. Take one representative but retain *all* members of its group as eligible next picks, along with the lower groups. At a tied gain all structured groups precede individually labeled exceptions: selecting a structured group therefore retains either all or none of each tied collection of exceptions. Once an exception is picked, no further symmetry is assumed. Gains cannot increase as the residual shrinks. Thus discarding a column whose gain fell to 14 cannot affect which column must be tried next unless the demand guard fires.

The final run visited **397,502** nodes. Its smallest demand was **15**. No omitted family could meet that demand, no full cover appeared, and the Fano upper bound passed. The [adversarial audit](AUDIT.md) used a different search organization and reached the same exclusion.

## Replay

From `econ-research/`, run:

```sh
PYTHONPATH=econ-lab/src python3 -m econ_lab verify balanced-ef2/check.py
```

Alternatively, run `python3 check.py` inside this directory (Python 3.10+, a C++20 compiler named `c++` or set `CXX`). The Python script regenerates the families without a solver library and builds `cover.cpp` in a temporary directory. Its JSON output binds the cover code and generated input by SHA-256; the harness also hashes the Python script. No download, GPU, random seed or saved solver state is required. [Receipt](RECEIPT.json) · [research ledger, stopping decision and method feedback](STATE.md).

Credit: original threshold, graph correspondence and upper construction belong to the cited authors. Local research, code and audit used OpenAI Codex Astra, Sol, Terra and Luna roles. Computational independence here means separate implementations and contexts, **not** outside human review. Kept local; not published.
