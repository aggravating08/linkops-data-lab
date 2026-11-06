FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 MPLBACKEND=Agg
RUN pip install --no-cache-dir pandas==2.2.3 matplotlib==3.10.1
RUN mkdir -p /opt/linkops /workspace && chown 65534:65534 /workspace
COPY sandbox/runner.py sandbox/probe.py /opt/linkops/
USER 65534:65534
WORKDIR /workspace
