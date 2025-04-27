# Research Topic: Metainformational Quantum Bridge (MQB) for SAT

## Title
Agentic Validation of the Metainformational Quantum Bridge (MQB) for SAT

## Keywords
SAT solving, Metainformational Quantum Bridge, matchgate, perfect matching, agentic pipeline, P=NP

## Abstract
The Metainformational Quantum Bridge (MQB) is a novel approach to solving Boolean satisfiability (SAT) problems by reducing them to perfect matching problems in planar graphs. This project aims to validate the MQB pipeline on a range of CNF formulas, benchmark its performance and correctness against established SAT solvers such as MiniSat, and analyze its potential implications for the P=NP question. The research will use a fully agentic, autonomous pipeline for experiment execution, result analysis, and report generation, following the AI Scientist-v2 methodology. Key objectives include verifying the correctness of MQB's SAT/UNSAT decisions, the accuracy of its assignment decoding, and its agreement with ground-truth solutions and MiniSat outputs.

## Motivation
SAT is a central NP-complete problem. If MQB can solve SAT efficiently via perfect matchings, it would have deep theoretical and practical significance. Validating MQB's claims requires rigorous, automated experimentation and benchmarking.

## Research Questions
- Does MQB correctly decide SAT/UNSAT for small and medium CNF instances?
- Are MQB's decoded assignments consistent with all satisfying assignments?
- How does MQB's performance and correctness compare to MiniSat?
- Can the agentic pipeline autonomously generate publishable reports from experiment results?

## Experiment Plan
- Implement the MQB pipeline (graph construction, planarization, orientation, Pfaffian decoding)
- Run MQB and MiniSat on batches of CNFs
- Analyze assignment agreement and SAT/UNSAT decision accuracy
- Generate plots and auto-write a scientific report

## Data
- Hand-crafted CNFs (from experiments/mqb/run_experiment.py)
- (Optional) Larger CNFs from SATLIB or other benchmarks

## Expected Output
- Structured experiment logs, result summaries, plots, and a Markdown report
- Automated validation of MQB claims
- Recommendations for further research
