ARG RAPIDS_IMAGE=rapidsai/base:26.08-cuda13-py3.12
FROM ${RAPIDS_IMAGE}
WORKDIR /workspace
COPY src/ src/
ENTRYPOINT ["python", "src/pipeline.py"]
