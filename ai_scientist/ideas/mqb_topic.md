# Research Topic: Metainformational Quantum Bridge (MQB) for SAT

## Title
Agentic Validation of the Metainformational Quantum Bridge (MQB) for SAT

## Keywords
SAT solving, Metainformational Quantum Bridge, matchgate, perfect matching, agentic pipeline, P=NP, variable-cycle, clause-gadget, planarity, Pfaffian

## Abstract
This project validates the MQB approach for SAT by implementing a classical SAT→PerfMatch reduction (variable-cycle gadgets, clause-OR gadgets, planarity, PSCG insertion, Kasteleyn orientation, Pfaffian computation, and proper decoding). We benchmark MQB against MiniSat on random and benchmark CNFs, analyze SAT/UNSAT agreement, assignment decoding, and runtime, and generate agentic reports.

## Motivation
Correct SAT→PerfMatch reduction is required for valid agentic benchmarking. Previous bipartite approaches fail for m > n. Classical gadget-based reduction (Lichtenstein/planar 3-SAT) ensures correctness and allows rigorous comparison to MiniSat.

## Research Questions
- Does MQB (with correct reduction) agree with MiniSat on SAT/UNSAT for random and benchmark CNFs?
- Is assignment decoding from PM reliable and consistent with MiniSat?
- What is the runtime and scaling behavior of the full MQB pipeline?
- Can the agentic pipeline autonomously generate publishable, debug-friendly reports?

## Experiment Plan
- Implement the correct SAT→PerfMatch reduction: variable-cycle gadgets for variables, clause-OR gadgets for clauses, with non-intersecting paths.
- Insert planarity gadgets (PSCG) at each crossing after building the SAT gadgets.
- Apply Kasteleyn orientation using a planarity embedding.
- Construct the Kasteleyn matrix K and compute Pf(K) via sqrt(det(K)). SAT iff Pf(K) ≠ 0.
- Extract a satisfying assignment from a perfect matching (PM) by decoding variable ports.
- Compare MQB SAT/UNSAT and assignments to MiniSat, and log all intermediate data (|V|, |E|, #PSCG, Pf(K)).

## Data
- Hand-crafted CNFs (from experiments/mqb/run_experiment.py)
- Random 3-SAT CNFs (n ≤ 20) for unit tests
- SATLIB and other benchmarks

## Expected Output
- Structured experiment logs, result summaries, plots, and a Markdown report
- Automated validation of MQB claims, including full debug dumps
- Recommendations for further research and debugging
