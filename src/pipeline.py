"""Run a small analytical pipeline on RAPIDS/CuPy or a dependency-free CPU backend."""

from __future__ import annotations

import argparse
import json
import random
import time


def cpu_pipeline(rows: int, seed: int = 7) -> dict:
    rng = random.Random(seed)
    started = time.perf_counter()
    groups: dict[int, list[float]] = {}
    for _ in range(rows):
        key = rng.randrange(16)
        groups.setdefault(key, []).append(rng.random())
    means = {key: sum(values) / len(values) for key, values in groups.items()}
    return {"backend": "cpu", "rows": rows, "groups": len(means), "checksum": round(sum(means.values()), 6), "elapsed_ms": round((time.perf_counter() - started) * 1000, 3)}


def gpu_pipeline(rows: int, seed: int = 7) -> dict:
    import cupy as cp
    import cudf

    started = time.perf_counter()
    rng = cp.random.RandomState(seed)
    frame = cudf.DataFrame({"group": rng.randint(0, 16, rows, dtype=cp.int32), "value": rng.random_sample(rows, dtype=cp.float32)})
    means = frame.groupby("group").value.mean()
    cp.cuda.Stream.null.synchronize()
    return {"backend": "rapids", "rows": rows, "groups": len(means), "checksum": round(float(means.sum()), 6), "elapsed_ms": round((time.perf_counter() - started) * 1000, 3)}


def run(rows: int, backend: str = "auto", seed: int = 7) -> dict:
    if rows <= 0 or backend not in {"auto", "cpu", "gpu"}:
        raise ValueError("rows must be positive and backend must be auto, cpu or gpu")
    if backend in {"auto", "gpu"}:
        try:
            return gpu_pipeline(rows, seed)
        except (ImportError, RuntimeError):
            if backend == "gpu":
                raise
    return cpu_pipeline(rows, seed)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=100000)
    parser.add_argument("--backend", choices=["auto", "cpu", "gpu"], default="auto")
    args = parser.parse_args()
    print(json.dumps(run(args.rows, args.backend), indent=2))


if __name__ == "__main__":
    main()
