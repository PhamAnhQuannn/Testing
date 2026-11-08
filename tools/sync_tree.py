"""Snapshot the parts of skill_tree.json and plan.json the app needs into content/index/.

    uv run python tools/sync_tree.py <skill_tree.json> <plan.json> [--out content/index]

Two selection rules feed the snapshot:
  1. The 40 MVP subtopics (SPEC 4.1): ids of plan days 1-12 in plan order, `bh.*` excluded, each
     counted once. These are the py/dsa/cs foundations.
  2. Two extra tracks selected whole by section/module, because they are NOT in the plan days:
     System Design (section `sd`, 86) and the AI-engineer LLM subset of `ml`
     (`ml.llm`, `ml.rag_agents`, `ml.llm_eval_serving`, `ml.system_design`, 39). They are appended
     after the 40 in tree order. These are concept tracks (SPEC 5.2); their prerequisites that fall
     outside the shipped set go to assumed.json (no plan `assumed_known` membership is required for
     this curated selection).

Every output file records the sha256 of its source files, so the committed snapshot shows which
version of the sources it was built from (CI cannot read them).
"""

import argparse
from pathlib import Path

from common import CONTENT, dump_json, load_json, sha256_file

MVP_LAST_DAY = 12
PLAN_SNAPSHOT_LAST_DAY = 14

# Extra tracks selected whole (not in the plan days).
EXTRA_SECTIONS = {"sd"}
EXTRA_MODULES = {"ml.llm", "ml.rag_agents", "ml.llm_eval_serving", "ml.system_design"}

# Individual nodes materialized beyond the MVP plan window (Wave 2+ fundamentals additions).
EXTRA_IDS = {
    "py.core.try_except_basics",
    "py.core.regex",
    "py.errors_modules.exceptions",
    "py.errors_modules.files_pathlib",
    "py.errors_modules.stdlib_tour",
    # Wave 2 Round 2: complete the py.oop module.
    "py.oop.inheritance_mro",
    "py.oop.dunder_methods",
    "py.oop.dataclasses_enums",
    "py.oop.equality_hashing_immutability",
    "py.oop.abc_protocols",
    # Wave 2 Round 3: complete py.functions + context managers.
    "py.functions.decorators",
    "py.functions.iterators_generators",
    "py.functions.itertools_idioms",
    "py.functions.functools_cache",
    "py.errors_modules.context_managers",
    # Wave 2 Round 4: complete py.advanced + type hints.
    "py.advanced.descriptors",
    "py.advanced.data_model_deep",
    "py.advanced.walrus_match_syntax",
    "py.typing_testing.type_hints",
    # Wave 2 Round 5: finish code-gradable py fundamentals (modules, logging, mocking).
    "py.errors_modules.modules_packages",
    "py.errors_modules.logging_debug",
    "py.typing_testing.mock_testability",
    # Wave 2 Round 6: DSA breadth - finish the started modules.
    "dsa.arrays_strings.matrix_traversal",
    "dsa.two_pointers_window.sliding_window_fixed",
    "dsa.two_pointers_window.sliding_window_variable",
    "dsa.linked_list.ll_fast_slow",
    "dsa.stack_queue.monotonic_stack",
    # Wave 2 Round 7: DSA breadth - heap module + binary search variants.
    "dsa.heap.heap_ds",
    "dsa.heap.heap_top_k",
    "dsa.heap.heap_advanced",
    "dsa.searching_sorting.binary_search_variants",
    "dsa.searching_sorting.binary_search_answer",
    # Wave 2 Round 8: DSA breadth - finish the trees module.
    "dsa.trees.tree_recursion",
    "dsa.trees.tree_bfs_views_hierarchy",
    "dsa.trees.bst",
    "dsa.trees.range_query_trees",
    # Wave 2 Round 9: DSA breadth - finish the graphs module.
    "dsa.graphs.graph_representation",
    "dsa.graphs.graph_traversal",
    "dsa.graphs.grid_graphs",
    "dsa.graphs.bfs_shortest_path",
    "dsa.graphs.topological_sort",
    "dsa.graphs.union_find",
    # Wave 2 Round 10: DSA breadth - finish the advanced_graphs module.
    "dsa.advanced_graphs.dijkstra",
    "dsa.advanced_graphs.bellman_ford_floyd",
    "dsa.advanced_graphs.mst",
    "dsa.advanced_graphs.graph_advanced_topics",
    # Wave 2 Round 11: DSA breadth - finish the dp module.
    "dsa.dp.dp_foundations",
    "dsa.dp.dp_1d",
    "dsa.dp.dp_knapsack",
    "dsa.dp.dp_strings",
    "dsa.dp.dp_grid",
    "dsa.dp.dp_state_machine",
    "dsa.dp.dp_interval",
    # Wave 2 Round 12: backtracking (finish recursion_backtracking) + tries module.
    "dsa.recursion_backtracking.backtracking_core",
    "dsa.recursion_backtracking.backtracking_constraints",
    "dsa.tries.trie_ds",
    "dsa.tries.trie_problems",
    # Wave 2 Round 13: finish the greedy_intervals module.
    "dsa.greedy_intervals.greedy_basics",
    "dsa.greedy_intervals.interval_basics",
    "dsa.greedy_intervals.interval_sweep",
    # Wave 2 Round 14: finish the design_ds module.
    "dsa.design_ds.design_cache",
    "dsa.design_ds.design_o1_structures",
    "dsa.design_ds.design_time_versioned",
    "dsa.design_ds.design_misc",
    # Wave 2 Round 15: finish the math_bits module.
    "dsa.math_bits.number_theory",
    "dsa.math_bits.bit_basics",
    "dsa.math_bits.geometry_random",
    # Wave 2 Round 16: practical systems (stateful class_ops).
    "dsa.practical.in_memory_store",
    "dsa.practical.bank_ledger_systems",
    "dsa.practical.file_system_sim",
    "dsa.practical.rate_limiters",
    # Wave 2 Round 17: practical parsing/IO.
    "dsa.practical.file_log_parsing",
    "dsa.practical.api_http_json",
    "dsa.practical.stream_iterator_processing",
    "dsa.practical.practical_format",
    # Wave 2 Round 18: practical eval engines.
    "dsa.practical.tokenizer_parser_interpreter",
    "dsa.practical.rules_engine_formulas",
    "dsa.practical.spreadsheet_formulas",
    "dsa.practical.simulation_state_machines",
    # Wave 2 Round 19: practical soft (oop + refactor/review + ai-assisted).
    "dsa.practical.oop_coding",
    "dsa.practical.refactor_debug_review",
    "dsa.practical.ai_assisted_coding",
    # Wave 2 Round 20: concurrency coding (concept-driven, deterministic simulations).
    "dsa.concurrency_coding.thread_safe_basics",
    "dsa.concurrency_coding.producer_consumer_pool",
    "dsa.concurrency_coding.concurrent_io_async",
    # Wave 3 Round 21: LLD OOP principles.
    "lld.oop_principles.pillars",
    "lld.oop_principles.solid",
    "lld.oop_principles.composition_vs_inheritance",
    # Wave 3 Round 22: LLD design patterns (creational + structural).
    "lld.patterns.creational_singleton_factory",
    "lld.patterns.structural_adapter_facade_proxy",
    "lld.patterns.structural_decorator_composite",
    # Wave 3 Round 23: LLD behavioral patterns (pattern_selection deferred to R26 for its prereqs).
    "lld.patterns.behavioral_strategy_state",
    "lld.patterns.behavioral_observer_command",
    "lld.patterns.behavioral_template_chain_iterator",
    # Wave 3 Round 24: LLD design process.
    "lld.process.requirements",
    "lld.process.entities_relationships",
    "lld.process.apis_code",
    "lld.process.extensibility",
    # Wave 3 Round 25: LLD classic problems A (stateful class_ops).
    "lld.problems.parking_lot",
    "lld.problems.vending_atm",
    "lld.problems.elevator",
    "lld.problems.library_booking_domain",
    # Wave 3 Round 26: LLD problems B + concurrency design + pattern selection (closes LLD).
    "lld.problems.ecommerce_ordering",
    "lld.problems.ride_hailing",
    "lld.problems.games",
    "lld.problems.logger_notification",
    "lld.concurrency_design.locking_booking",
    "lld.patterns.pattern_selection",
    # Wave 4 Round 27: ML foundations - math A (pure-Python, by-hand on lists).
    "ml.math.algebra_functions_bridge",
    "ml.math.linear_algebra_basics",
    "ml.math.derivatives_gradients",
    "ml.math.gradient_descent",
    # Wave 4 Round 28: ML foundations - math B (probability + distributions + eigen).
    "ml.math.probability_basics",
    "ml.math.random_variables_expectation",
    "ml.math.distributions",
    "ml.math.linalg_decomposition",
    # Wave 4 Round 29: ML foundations - math C (closes ml.math: MLE/entropy/inference/A-B).
    "ml.math.mle_map",
    "ml.math.entropy_kl",
    "ml.math.statistical_inference",
    "ml.math.ab_testing",
    # Wave 4 Round 30: ML foundations - fundamentals A (Q253 write_code in classification_metrics).
    "ml.fundamentals.ml_overview",
    "ml.fundamentals.loss_functions",
    "ml.fundamentals.bias_variance_overfitting",
    "ml.fundamentals.classification_metrics",
    # Wave 4 Round 31: ML foundations - fundamentals B (closes ml.fundamentals).
    "ml.fundamentals.calibration",
    "ml.fundamentals.regression_ranking_metrics",
    "ml.fundamentals.validation_tuning",
    "ml.fundamentals.interpretability_fairness",
    # Wave 4 Round 32: ML foundations - classical A (OLS/logistic/trees/ensembles). knn_nb_svm and
    # unsupervised deferred: their assessment write_code (Q240/Q241) references use numpy, which the
    # stdlib-only Pyodide harness cannot run as a generated check solution.
    "ml.classical.linear_regression",
    "ml.classical.logistic_regression",
    "ml.classical.decision_trees",
    "ml.classical.ensembles",
    # Wave 4 Round 33: ML foundations - classical B (closes ml.classical pure-Python subset).
    "ml.classical.dimensionality_reduction",
    "ml.classical.recsys_algorithms",
    "ml.classical.time_series_anomaly",
    # Wave 4 Round 34: ML foundations - NLP & Transformers A (opens ml.nlp_transformers).
    "ml.nlp_transformers.classic_nlp",
    "ml.nlp_transformers.tokenization",
    "ml.nlp_transformers.embeddings",
    # Wave 4 Round 35: ML foundations - NLP & Transformers B (closes ml.nlp_transformers + Wave 4).
    "ml.nlp_transformers.attention",
    "ml.nlp_transformers.transformer_architecture",
    "ml.nlp_transformers.transformer_variants",
    # Wave 5 Round 36: Python breadth - runtime + core (opens py.runtime).
    "py.runtime.memory_gc",
    "py.runtime.gil",
    "py.runtime.performance",
    "py.core.io_input",
    # Wave 5 Round 37: Python breadth - concurrency + packaging (opens py.concurrency).
    "py.concurrency.threading",
    "py.concurrency.asyncio_basics",
    "py.concurrency.multiprocessing",
    "py.typing_testing.envs_packaging",
    # Wave 5 Round 38: Python breadth - testing + net + db (opens py.ecosystem).
    "py.typing_testing.pytest_testing",
    "py.errors_modules.http_requests",
    "py.ecosystem.db_python",
    # Wave 5 Round 39: Python breadth - ecosystem data (numpy/pandas/viz).
    "py.ecosystem.numpy_basics",
    "py.ecosystem.pandas_basics",
    "py.ecosystem.pandas_transform",
    "py.ecosystem.notebooks_viz",
    # Wave 5 Round 40: Python breadth - ecosystem web/ai (closes py).
    "py.ecosystem.fastapi",
    "py.ecosystem.flask",
    "py.ecosystem.django",
    "py.ecosystem.ai_python_stack",
    # Wave 6 Round 41: cs.sql A (opens cs.sql — real sqlite3 grading).
    "cs.sql.intro",
    "cs.sql.select_where",
    "cs.sql.aggregation",
    "cs.sql.joins",
    # Wave 6 Round 42: cs.sql B (closes cs.sql — subqueries/windows/dml/puzzles).
    "cs.sql.subqueries_sets",
    "cs.sql.window_functions",
    "cs.sql.dml_ddl",
    "cs.sql.classic_puzzles",
    # Wave 7 Round 43: cs.databases A (concept, opens cs.databases).
    "cs.databases.relational_basics",
    "cs.databases.normalization",
    "cs.databases.indexing_btree",
    "cs.databases.transactions_acid",
    # Wave 7 Round 44: cs.databases B (concept, isolation/locking/nosql/query-opt).
    "cs.databases.isolation",
    "cs.databases.locking_mvcc",
    "cs.databases.nosql",
    "cs.databases.query_optimisation",
}

# Expected shipped counts, asserted so an upstream tree edit can't silently change the snapshot.
PLAN_MVP_COUNT = 40
EXPECTED_SD = 86
EXPECTED_ML4 = 39
EXPECTED_EXTRA_IDS = len(EXTRA_IDS)  # Wave 2 additions
EXPECTED_TOTAL = PLAN_MVP_COUNT + EXPECTED_SD + EXPECTED_ML4 + EXPECTED_EXTRA_IDS  # 341

# Node fields the app uses (SPEC 4.2); optional ones are skipped when a node lacks them.
NODE_FIELDS = [
    "name_vi", "order", "summary_vi", "mastery_bar_vi", "prerequisites", "lang_prereqs",
    "key_concepts", "concepts_vi", "examples_vi", "beginner_note_vi", "starter_code_vi",
    "example_problems", "bank_topics", "bank_counts", "target_swe", "target_ai",
    "est_hours", "est_hours_beginner",
]  # fmt: skip


def flatten(tree: dict) -> dict[str, tuple[str, str, dict]]:
    """id -> (section_id, module_id, node), in tree order."""
    return {
        sub["id"]: (section["section"]["id"], module["id"], sub)
        for section in tree["sections"]
        for module in section["modules"]
        for sub in module["subtopics"]
    }


def mvp_ids(plan: dict) -> list[str]:
    ids: list[str] = []
    for day in plan["days"][:MVP_LAST_DAY]:
        for sub in day["subtopics"]:
            if not sub["id"].startswith("bh.") and sub["id"] not in ids:
                ids.append(sub["id"])
    return ids


def selected_ids(nodes: dict[str, tuple[str, str, dict]], plan: dict) -> list[str]:
    """The plan-day MVP ids (rule 1), then the extra-track ids (rule 2).

    Rule 2 keeps modules in their tree appearance order but orders subtopics WITHIN a module by the
    node's authored ``order`` field, not the raw list order. The list order sometimes disagrees with
    ``order`` (e.g. sd.archetypes lists metrics_logging before its prerequisite data_pipeline),
    which otherwise produced a prerequisite-after-dependent pair in the generated plan order.
    """
    ids = mvp_ids(plan)
    seen = set(ids)
    extra = [
        (sub_id, module, node)
        for sub_id, (section, module, node) in nodes.items()
        if sub_id not in seen
        and (section in EXTRA_SECTIONS or module in EXTRA_MODULES or sub_id in EXTRA_IDS)
    ]
    module_pos: dict[str, int] = {}
    for _sub_id, module, _node in extra:
        module_pos.setdefault(module, len(module_pos))
    extra.sort(key=lambda t: (module_pos[t[1]], t[2].get("order", 0)))
    for sub_id, _module, _node in extra:
        ids.append(sub_id)
        seen.add(sub_id)
    return ids


def prerequisites_of(node: dict) -> set[str]:
    lang = node.get("lang_prereqs") or {}
    return set(node.get("prerequisites") or []) | set(lang.get("python") or [])


def build_subtopics(nodes: dict[str, tuple[str, str, dict]], plan: dict) -> list[dict]:
    plan_hours = {k["id"]: k["plan_hours"] for k in plan["selection"]["kept"]}
    first_day: dict[str, int] = {}
    for day in plan["days"][:MVP_LAST_DAY]:
        for sub in day["subtopics"]:
            first_day.setdefault(sub["id"], day["day"])
    subtopics = []
    for position, sub_id in enumerate(selected_ids(nodes, plan), start=1):
        section, module, node = nodes[sub_id]
        subtopics.append(
            {"id": sub_id, "section": section, "module": module}
            | {f: node[f] for f in NODE_FIELDS if f in node}
            | {
                "plan_order": position,
                # Extra-track subtopics are not in the plan days: no plan_day, est_hours as hours.
                "plan_day": first_day.get(sub_id),
                "plan_hours": plan_hours.get(sub_id, node.get("est_hours", 0)),
            }
        )
    return subtopics


def build_assumed(subtopics: list[dict], nodes: dict[str, tuple[str, str, dict]]) -> list[str]:
    """Prerequisites of shipped subtopics that are not themselves shipped (SPEC 5.3 unlock).

    For the curated section/module selection these are simply listed as assumed-known; a prereq
    that is not a real tree node is a data error and fails the sync.
    """
    shipped = {s["id"] for s in subtopics}
    outside = sorted({p for s in subtopics for p in prerequisites_of(s)} - shipped)
    missing = [p for p in outside if p not in nodes]
    if missing:
        raise SystemExit(f"prerequisites not found in the skill tree: {missing}")
    return outside


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("skill_tree", type=Path)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--out", type=Path, default=CONTENT / "index")
    args = parser.parse_args()

    tree, plan = load_json(args.skill_tree), load_json(args.plan)
    nodes = flatten(tree)
    subtopics = build_subtopics(nodes, plan)

    sd = sum(1 for s in subtopics if s["section"] in EXTRA_SECTIONS)
    ml4 = sum(1 for s in subtopics if s["module"] in EXTRA_MODULES)
    extra_ids = sum(1 for s in subtopics if s["id"] in EXTRA_IDS)
    plan_count = len(subtopics) - sd - ml4 - extra_ids
    got = (plan_count, sd, ml4, extra_ids, len(subtopics))
    want = (PLAN_MVP_COUNT, EXPECTED_SD, EXPECTED_ML4, EXPECTED_EXTRA_IDS, EXPECTED_TOTAL)
    if got != want:
        raise SystemExit(
            f"unexpected counts (plan, sd, ml4, extra_ids, total): got {got}, expected {want}"
        )

    hashes = {"skill_tree.json": sha256_file(args.skill_tree), "plan.json": sha256_file(args.plan)}
    args.out.mkdir(parents=True, exist_ok=True)
    outputs = {
        "subtopics.json": {"source_hash": hashes, "subtopics": subtopics},
        "plan.json": {"source_hash": hashes, "days": plan["days"][:PLAN_SNAPSHOT_LAST_DAY]},
        "assumed.json": {"source_hash": hashes, "assumed": build_assumed(subtopics, nodes)},
    }
    for name, data in outputs.items():
        (args.out / name).write_text(dump_json(data), encoding="utf-8")
    print(f"wrote {', '.join(outputs)} to {args.out} ({len(subtopics)} subtopics)")


if __name__ == "__main__":
    main()
