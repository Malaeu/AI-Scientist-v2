import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import networkx as nx
from experiments.mqb.mqb_core import build_matchgate_graph, planarise_with_pscg, kasteleyn_orient, pfaffian_decision_and_decode

def run_mqb_on_dimacs(dimacs_path, debug_dump_path=None):
    """Run MQB pipeline on a DIMACS CNF file and dump debug info."""
    # Parse DIMACS
    cnf = []
    with open(dimacs_path) as f:
        for line in f:
            if line.startswith('p') or line.startswith('c') or not line.strip():
                continue
            clause = tuple(int(x) for x in line.strip().split() if x != '0')
            if clause:
                cnf.append(clause)
    # MQB pipeline
    G = build_matchgate_graph(cnf)
    Gp = planarise_with_pscg(G)
    Go = kasteleyn_orient(Gp)
    is_sat, assignment = pfaffian_decision_and_decode(Go, debug_dump_path=debug_dump_path)
    return is_sat, assignment

if __name__ == "__main__":
    # Example usage on the test file
    is_sat, assignment = run_mqb_on_dimacs("ai_scientist/ideas/test_unsat_vs_sat.cnf", debug_dump_path="ai_scientist/ideas/test_unsat_vs_sat.mqb_dump.json")
    print(f"MQB SAT: {is_sat}\nAssignment: {assignment}")
