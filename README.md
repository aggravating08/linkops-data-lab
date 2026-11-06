# LinkOps Data Lab

**Ask a question about a CSV. See the plan, inspect the Python, and get a result produced inside a fresh, network-isolated Vultr sandbox.**

LinkOps Data Lab is a containment-first CSV analyst for the LabLab × Vultr Agent Rush **Blast Radius Zero** challenge. Vultr Serverless Inference turns a plain-language question into a short execution plan and Python script. The backend dispatches that script to a disposable Docker container on Vultr Cloud Compute, then asks the model to explain the actual stdout returned by the run. The result and generated code are shown together so a reviewer can verify what happened.

## Product flow

1. The user uploads or pastes a CSV and asks a question.
2. After the user checks the data-handling consent, the backend sends the question, column names, and up to five preview rows to Vultr Serverless Inference. The full CSV is never placed in the prompt.
3. The model returns a plan and Python source. The source is displayed in the result.
4. The backend creates a unique Docker volume and starts a fresh sandbox container. The full CSV and script are staged in that volume.
5. The script runs with no network, a read-only root filesystem, a non-root UID, no Linux capabilities, a 512 MB memory limit, a half-CPU limit, a 48-process limit, and a 15-second execution deadline. Only the temporary task volume is writable. No API key or environment secret is passed into the sandbox.
6. The app returns the sandbox's actual stdout and optional Matplotlib chart. A second Vultr Inference call summarizes that output. Containers and the task volume are deleted in a `finally` cleanup path.

The planner uses an LLM and the contained Python run produces real output. The sandbox boundary is the security control; prompt instructions and AST checks are defense in depth, not a claim that generated code is safe by itself. This is a hackathon prototype, not a hardened multi-tenant service. Do not upload confidential, regulated, or personal data.

## Run locally

Requirements: Docker Engine with Compose, plus a Vultr Serverless Inference API key. Create a local `.env` from `.env.example` and keep the key out of source control.

```sh
cp .env.example .env
# Edit .env and set VULTR_INFERENCE_API_KEY and LINKOPS_DOMAIN.
docker compose up -d --build
```

For a local-only HTTP demo, set `LINKOPS_DOMAIN=:8080`, change the Caddy port mapping in `compose.yaml` to `8080:80`, and open `http://localhost:8080`. The same-origin check remains enabled. A model request is billed by Vultr Serverless Inference; track usage in the Vultr console.

## Vultr deployment

The hackathon requires both the web app and backend on a Vultr VM. This project uses a small Ubuntu Cloud Compute instance, Docker Compose, Caddy HTTPS, and Vultr Serverless Inference. The public deployment should use a DNS name resolving to the VM; for a short demo, a `nip.io` hostname can resolve to the public IP while Caddy obtains TLS.

1. Confirm the LabLab submission is registered and the $200 hackathon credit is visible in Vultr Billing.
2. In Vultr Serverless Inference, create a subscription/key with the lowest-cost suitable chat model. Copy the key directly into a server-side `.env` file with mode `0600`. Never commit it, print it, pass it to the browser, or add it to the sandbox environment.
3. Create one small Cloud Compute VM using the hackathon credit only. If Vultr requests a payment method or any personal payment, stop. Open only TCP 22, 80, and 443 in the firewall.
4. Install Docker Engine and Compose, copy or clone this repository to the VM, and create `/opt/linkops/.env` with the public hostname, Docker socket group ID, and inference key.
5. Build and start with `docker compose up -d --build`. The first build downloads the app and sandbox images. Confirm `https://YOUR_HOST/health` and run the sample CSV through the public UI.
6. Review Vultr Remaining Credit and usage. Delete the VM and the inference subscription after judging or when you no longer need the demo. No personal payment method is required for this project and none should be added.

Example configuration (replace values locally; do not commit):

```dotenv
LINKOPS_DOMAIN=PUBLIC_IP.nip.io
DOCKER_GID=999
VULTR_INFERENCE_API_KEY=secret-from-vultr-console
VULTR_INFERENCE_MODEL=deepseek-v4.1-flash-1017
```

The app needs access to `/var/run/docker.sock` to create and remove task containers. Docker socket access is highly privileged and must remain confined to this single-purpose app on the Vultr VM. The sandbox containers do not mount the socket.

## API

- `GET /health` — web service and inference-key configuration status; never returns the key.
- `GET /api/runs` — short-lived in-memory run summaries only.
- `POST /api/run` — JSON body `{ "question": "...", "csv": "..." }`; returns plan, Python, sandbox output, optional chart, and run metadata.

CSV limit: 500 KB, 20,000 data rows, and 40 unique columns. The service allows two concurrent runs and rate-limits mutations. Request bodies and CSV contents are not written to app logs or the summary list. The uploaded file is transferred to a per-run Docker volume, destroyed after execution, and not persisted by the app.

## Project status and demo

- Source has been reworked for the official Blast Radius Zero brief.
- A public demo, public repository, Vultr VM deployment, live inference key, and demo video must each be verified before claiming they are live.
- The LabLab entry must be submitted on the LabLab platform; Vultr Community sharing is optional and does not replace it.
- Submission requirements include a public GitHub repo, Vultr VM backend, public demo URL, recorded demo with a containment moment, and clear architecture/use-case explanation.
- [Submission cover image](assets/linkops-cover.png)
- [Five-slide presentation](output/pdf/LinkOps_Presentation.pdf)
- [Demo recording script](DEMO_SCRIPT.md)

## Technology

- Vultr Cloud Compute (web app, orchestration backend, Docker host)
- Vultr Serverless Inference (plan/code generation and post-run explanation)
- Docker, Python, pandas, Matplotlib, SQLite-free transient run summaries
- Caddy (HTTPS reverse proxy)

## License

MIT. See [LICENSE](LICENSE).

## Event

- [Vultr: Agent Rush Hackathon](https://lablab.build/ai-hackathons/vultr-hackathon)
- [LinkOps LabLab team page](https://lablab.build/ai-hackathons/vultr-hackathon/linkops)
