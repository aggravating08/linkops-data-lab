# LinkOps Data Lab demo (about 2 minutes)

Record this with the deployed public HTTPS app and keep the live Vultr URL visible. Use the built-in sample CSV; do not upload personal or confidential data.

1. **Introduce the workflow (15 sec).** “LinkOps Data Lab turns a plain-language question into a plan, generated Python, and a result that was actually executed. Vultr Inference plans and writes; each run is dispatched to a separate sandbox on Vultr.”
2. **Run a real analysis (35 sec).** Select **Load sample CSV**. Ask “Which product generated the most revenue? Show a chart.” Check the data-handling consent and run it. Show the plan, chart, sandbox stdout, and Python returned by the run. State that the preview (headers and five rows) goes to Vultr Inference and the full CSV stays in the temporary sandbox volume.
3. **Show the boundary (30 sec).** Select **Run isolation probe**. Point to the actual network-denied check, read-only root write denial, and “Inference key NOT PRESENT” result. Explain that the probe uses a separate disposable container and does not attempt destructive activity.
4. **Show the architecture (20 sec).** Explain: Caddy HTTPS → Vultr VM app/orchestrator → Vultr Serverless Inference for planning and explanation → fresh Docker container with no network, bounded memory/CPU/time, non-root UID and an ephemeral task volume. No API secret is passed to the sandbox.
5. **Close with honest limits (10 sec).** State that this is a hackathon prototype, input data should be non-sensitive, and it is not a hardened multi-tenant service.

Do not claim a stage completed until its result is visible on screen. If a live inference request fails, show the actual error and do not use fixtures as though they were live results.
