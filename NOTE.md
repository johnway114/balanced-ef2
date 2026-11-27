# Twelve people suffice for balanced EF2 on at most ten goods

**Status.** Unrefereed, computer-assisted, not independently reviewed by a human.

On at most ten indivisible goods, twelve people in any two prescribed nonempty groups are guaranteed a balanced EF2 split, provided every valuation is monotone. This narrows the ten-good chromatic interval of Alipour and Jafari from [10, 14] to {13, 14}. The result does not settle the all-goods question for ten people, does not determine whether thirteen people can fail on ten goods, and is not a priority claim.

## Problem

Alipour and Jafari ([arXiv:2611.04486](https://arxiv.org/abs/2611.04486)) study the allocation of indivisible goods between two prescribed nonempty groups. Each person must weakly prefer their group's bundle to the other bundle after deleting at most two goods of their choice from the comparison bundle (EF2). The two bundles must differ in size by at most one (balanced). Valuations are monotone — nobody values a bundle less when a good is added — but need not be additive.

They prove that nine people always succeed, for any number of goods, and that fourteen can fail. The corresponding graph is the generalised Kneser graph KG(2n, n, 3), whose vertices are the n-subsets of a 2n-element set, with edges joining sets that share at most two elements. For every n ≥ 4 they obtain 10 ≤ χ(KG(2n, n, 3)) ≤ 14, with equality to 14 at n = 4 (eight goods). The value at ten goods (n = 5), and whether ten people always succeed with no bound on the number of goods, were left open.

## Result

An exact computer search, recorded below, rules out every cover of KG(10, 5, 3) by twelve independent sets. Because the agent threshold is strict, this guarantees a balanced EF2 split for twelve people with monotone valuations on ten goods, including every nonempty group-size split. The known fourteen-class Fano cover of Balogh, Cherkashin and Kiselev still shows that fourteen people can fail. Hence χ(KG(10, 5, 3)) ∈ {13, 14}.

An irrelevant dummy good transfers existence from an even goods count to the preceding odd count, and the same guarantee therefore holds for every goods count up to ten. (On eight goods the cited paper already gives exactly fourteen colours; on six goods the graph is complete on twenty vertices; with at most four goods any balanced comparison bundle can be deleted.) For an unbounded number of goods the known agent interval remains [9, 13].

## Method

On 2k goods, a balanced allocation may be represented by the k goods given to the first group. Two allocations are adjacent when their sets share at most two goods. A single agent cannot reject two adjacent allocations, and a second-group agent is represented by complements. Thus a failure for twelve agents would be a cover of the graph by twelve independent sets. Conversely, every independent set can be realised as a rejection family by a monotone binary valuation (Alipour–Jafari, Theorem 2.1).

Independent sets in KG(10, 5, 3) are families of five-subsets that meet pairwise in at least three elements. The checker classifies all large such families: every independent class has size at most 14, or can be enlarged into one of 492 structured families (triple stars, radius-one balls, and complements of triple stars) or one of 33,600 exceptional families of size 18. A colouring can be tested as a cover, since overlaps may be assigned to one of their covering classes.

The search then excludes every twelve-class cover. With N vertices still uncovered and q slots left, some remaining class must cover at least ceil(N/q) of them. If this demand ever reaches 14 or less, the search stops with an error, not a proof, because an omitted family might meet the demand. The archived run's minimum demand was 15, against an omitted-size upper bound of 14. The known fourteen-class Fano cover is replayed as a check, rather than treated as a search result.

The C++ search uses a symmetry reduction on residual cell partitions; the invariant and the branching rule are written out in the [README](README.md). The final run visited 397,502 nodes and found no cover.

## Two written results for any number of goods

These are unrefereed written proofs, not machine-formalised.

- If each person's valuation depends on at most four specified goods, ten people always succeed, even when the supports differ and the valuations are not additive. See [FOUR-GOOD-SUPPORT.md](FOUR-GOOD-SUPPORT.md).
- Any six approval lists can be balanced so that the two counts on each list differ by at most two. This covers any number of people whose valuations depend monotonically on those counts, and even one additional person with an unrestricted monotone valuation, who may choose the orientation. Seven lists can fail simultaneous balance; that is not a ten-person impossibility. See [SIX-LISTS.md](SIX-LISTS.md).

## Archived receipt

The following figures are copied verbatim from [RECEIPT.json](RECEIPT.json), produced by `check.py` on 27 November 2026 at 01:44:17 UTC. The script SHA-256 was `683376690363e95f6d8aa5434c285a936809747f63ac7d557c331b95a7c4a87f`; the run passed with exit code 0 in 2.2223 seconds on Python 3.14.7, platform `macOS-26.5.2-arm64-arm-64bit-Mach-O`. Standard output:

```json
{"anchored_maximal_families_by_size": {"7": 36, "10": 882, "12": 1098, "14": 900, "18": 230, "21": 2, "26": 4}, "cover_proof": {"compiler": "Apple clang version 21.0.0 (clang-2100.1.1.101)", "cover_source_sha256": "e2db46fbce060e10c37dade27483f8de582227f041a892f8e9f623b138be899b", "excluded_colors": 12, "input_sha256": "1bcc48ffa94d68c2658da894ed566b2878bbd9db2af9ec18da8392acbbd310e1", "minimum_demand": 15, "nodes": 397502}, "fano_cover_size": 14, "omitted_size_upper_bound": 14, "other_large_classes": 33600, "six_list_max_bad_choices_per_row": {"6": 2, "7": 5}, "structured_classes": 492, "vertices": 252}
```

## How to reproduce

From this directory, with Python 3.10 or later and a C++20 compiler named `c++` (or set `CXX`):

```sh
python3 check.py
```

The script regenerates the families, compiles `cover.cpp` in a temporary directory, and prints the JSON above. No download, GPU, random seed or saved solver state is required. An alternative, from the parent `econ-research/` directory if `econ-lab` is present, is `PYTHONPATH=econ-lab/src python3 -m econ_lab verify balanced-ef2/check.py`.

A replay of `python3 check.py` on the same machine on 27 November 2026 reproduced the archived standard output, including both SHA-256 hashes, in 2.67 seconds.

## Limitations and risks

- The C++ symmetry reduction has been audited in writing only. It has not been machine-formalised.
- The two all-goods special-case proofs are written arguments, not formalised.
- Monotonicity is essential. Without it, even two people can fail: there is a (non-monotone) ten-good example in the [audit](AUDIT.md).
- A separate thirteen-colour run is exploratory. It is not an exclusion and is not part of the proof receipt. Whether thirteen people can fail on ten goods remains open.
- The all-goods question for ten people remains open. The ten-good theorem does not lift to more goods: the balanced-deletion map runs from larger goods graphs to smaller ones, and the finite lower bound is not universal.
- An independent in-session Python search reproduced the twelve-colour exclusion, but this is AI-assisted internal verification, not external confirmation. A separate answer-blind reconstruction obtained the weaker interval [12, 14] and did not by itself exclude twelve arbitrary families.
- No matching published lower bound of 13 on ten goods was located in the literature check recorded in [SOURCES.md](SOURCES.md). That check is not a priority certificate.

## Credit

Original threshold, graph correspondence and upper construction belong to the cited authors. Local research, code and audit used OpenAI Codex Astra, Sol, Terra and Luna roles, as recorded in the project README. Computational independence here means separate implementations and contexts, not outside human review.

## References

- Sharareh Alipour and Amir Jafari, *Balanced Fair Division and Generalized Kneser Graphs*, [arXiv:2611.04486](https://arxiv.org/abs/2611.04486).
- Balogh, Cherkashin and Kiselev, [arXiv:1805.09394](https://arxiv.org/abs/1805.09394).
- Kyropoulou, Suksompong and Voudouris, [doi:10.1016/j.tcs.2020.07.008](https://doi.org/10.1016/j.tcs.2020.07.008).
