# Metainformational Quantum Bridge (MQB): Structured Experiment Proposal

## Objective
To experimentally validate the MQB algorithm for SAT and related NP-complete problems, focusing on:
- Correctness of the cross-gadget bijection
- Efficient planarization and Kasteleyn orientation
- Direct decoding of assignments from the Pfaffian
- Empirical scaling and practical feasibility

## Experimental Pipeline

### 1. Formal Gadget Validation
- Prove (or empirically validate) that the cross-gadget maintains a bijection of perfect matchings.
- Use small test graphs to exhaustively enumerate matchings before/after gadget insertion.
- Automate checks for edge cases and signature preservation.

### 2. Planarization Implementation
- Implement planarization with cross-gadgets for arbitrary SAT graph encodings.
- Use the Boyer–Myrvold planarity test for verification.
- Benchmark time and memory usage for graphs up to 10⁴ vertices.

### 3. Kasteleyn Orientation
- Implement or adapt an efficient algorithm for Kasteleyn orientation on planar graphs.
- Verify correctness by checking Pfaffian sign consistency and matching counts.

### 4. Pfaffian-Based Decoding
- Implement O(n³) decoding of SAT assignments via the Pfaffian adjugate (no Blossom V).
- Validate that decoded assignments correspond to valid SAT solutions on benchmark instances.

### 5. Benchmarking and Validation
- Use standard SAT benchmarks (e.g., SATLIB uf20–uf150 series).
- Compare MQB performance to MiniSat and/or other SAT solvers for correctness and speed.
- Record wall-clock time, memory use, and scaling behavior.
- Document any anomalies or deviations from theoretical predictions.

### 6. Reporting and Review
- Synthesize results into a structured report: correctness, complexity, and open issues.
- Highlight any unresolved theoretical or practical blockers.
- Prepare for external peer review and publication if results are positive.

## Immediate Action Items
1. Prototype and test cross-gadget validation code.
2. Implement planarization and Kasteleyn orientation pipeline for small-to-medium SAT instances.
3. Integrate Pfaffian-based decoding and validate on known solutions.
4. Begin benchmarking and collect empirical data.

## Open Questions
- Are there rare edge cases where the gadget bijection fails?
- Can Kasteleyn orientation be efficiently maintained during iterative planarization?
- How does numerical stability affect Pfaffian-based decoding on large instances?
- What are the practical limits of scalability before theoretical polynomial bounds break down?

---

This proposal provides a step-by-step experimental roadmap for the MQB algorithm, ensuring that both theoretical and practical aspects are rigorously validated. Results will inform further development and potential publication.
