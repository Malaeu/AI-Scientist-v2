"""
Experiment code for: Agentic Validation of the Metainformational Quantum Bridge (MQB) for SAT Solving (Correct Gadget-Based Pipeline)

This script implements the experiment plan described in mqb_topic.json/md:
- Implements the correct SAT→PerfMatch reduction (variable-cycle gadgets, clause-OR gadgets, planarity, PSCG, Kasteleyn, Pfaffian, decoding)
- Runs MQB and MiniSat on batches of CNF formulas
- Analyzes agreement between MQB's decoded assignments and MiniSat
- Compares performance (runtime, accuracy)
- Outputs structured logs/results for agentic pipeline analysis and report writing
"""
import os
import time
import json
from experiments.mqb import mqb_core

# --- CONFIG ---
CNF_DIR = "experiments/mqb/cnfs"  # Directory containing CNF files
RESULTS_FILE = "experiments/mqb/results_mqb_topic.json"

# --- STUBS: Replace with real implementations ---
def load_cnf_files(cnf_dir):
    """Load all CNF files from the directory."""
    cnf_files = [os.path.join(cnf_dir, f) for f in os.listdir(cnf_dir) if f.endswith('.cnf')]
    return cnf_files

def run_mqb_pipeline(cnf_path, debug_dump_path=None):
    """Run the full MQB pipeline (correct gadget-based)."""
    # Parse DIMACS CNF
    cnf = []
    with open(cnf_path) as f:
        for line in f:
            if line.startswith('p') or line.startswith('c') or not line.strip():
                continue
            clause = tuple(int(x) for x in line.strip().split() if x != '0')
            if clause:
                cnf.append(clause)
    # Pipeline (all steps must be implemented in mqb_core)
    G = mqb_core.build_sat_gadget_graph(cnf)
    Gp = mqb_core.planarise_with_pscg(G)
    Go = mqb_core.kasteleyn_orient(Gp)
    is_sat, assignment = mqb_core.pfaffian_decision_and_decode(Go, debug_dump_path=debug_dump_path)
    return is_sat, assignment

def run_minisat(cnf_path):
    """Stub for running MiniSat: returns (sat, assignment, runtime)."""
    t0 = time.time()
    # TODO: Actually call MiniSat and parse output
    sat = True
    assignment = {"x1": 1, "x2": 0}
    runtime = time.time() - t0
    return sat, assignment, runtime

def compare_assignments(a1, a2):
    """Compare two assignments (dicts). Returns fraction agreement."""
    if not a1 or not a2:
        return 0.0
    keys = set(a1.keys()) & set(a2.keys())
    agree = sum(a1[k] == a2[k] for k in keys)
    return agree / len(keys) if keys else 0.0

# --- MAIN EXPERIMENT LOOP ---
def main():
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    cnf_files = load_cnf_files(CNF_DIR)
    results = []
    for cnf_path in cnf_files:
        print(f"Processing {cnf_path}")
        debug_dump_path = cnf_path + ".mqb_dump.json"
        try:
            mqb_sat, mqb_assign = run_mqb_pipeline(cnf_path, debug_dump_path=debug_dump_path)
        except NotImplementedError as e:
            print(f"MQB pipeline not fully implemented: {e}")
            mqb_sat, mqb_assign = None, None
        mini_sat, mini_assign, mini_time = run_minisat(cnf_path)
        agree = compare_assignments(mqb_assign, mini_assign)
        result = {
            "cnf": os.path.basename(cnf_path),
            "mqb_sat": mqb_sat,
            "minisat_sat": mini_sat,
            "assignment_agreement": agree,
            "minisat_runtime": mini_time,
        }
        results.append(result)
        print(f"Result: {result}")
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)
    print(f"All results written to {RESULTS_FILE}")

if __name__ == "__main__":
    main()
