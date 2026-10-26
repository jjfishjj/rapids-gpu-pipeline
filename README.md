# RAPIDS GPU Pipeline

同一支 pipeline 支援 dependency-free CPU 基準與真實 cuDF／CuPy GPU 執行，用來驗證資料常駐、groupby 工作負載與端到端加速，而不只比較單一 kernel。

## CPU 與單元測試

```bash
python -m unittest discover -s tests -v
python src/pipeline.py --rows 100000 --backend cpu
```

## NVIDIA 實機

建議在 NVIDIA RAPIDS container 或對應 CUDA 環境安裝 `requirements-gpu.txt`：

```bash
python src/pipeline.py --rows 10000000 --backend gpu
```

推薦的可重現執行方式：

```bash
docker build -t nvidia-lab/rapids .
docker run --rm --gpus all --ipc=host nvidia-lab/rapids --rows 10000000 --backend gpu
```

Dockerfile 固定 RAPIDS 26.08、CUDA 13、Python 3.12；CUDA 12 使用 `requirements-gpu.txt`，CUDA 13 使用 `requirements-gpu-cu13.txt`。

`auto` 優先使用 GPU、缺少 RAPIDS 時退回 CPU；`gpu` 在 GPU stack 不完整時直接失敗，適合 CI 驗收。自架 GPU Runner 可手動執行 `gpu.yml`。

## 痛點檢查

- 不要在每一步呼叫 `.to_pandas()`／`.get()`。
- 將 ingest、轉換、聚合、模型與輸出視為同一條 pipeline。
- 先觀察資料是否裝得進 GPU，再決定分批、RMM pool 或 Dask-CUDA。

