# RunPod

## Local CLI setup

```bash
pixi global install runpodctl
runpodctl update
runpodctl doctor
```

The lab uses a shared RunPod API key tied to the common compute pool. Treat it like a password; never commit it or post it publicly.

## Useful commands

```bash
runpodctl gpu list
runpodctl datacenter list
runpodctl pod list
runpodctl pod list --all
runpodctl pod get <pod-id>
runpodctl pod logs <pod-id> --follow
runpodctl ssh info <pod-id>
runpodctl pod start <pod-id>
runpodctl pod stop <pod-id>
runpodctl pod delete <pod-id>
```

## Lab defaults

- One GPU unless the experiment needs more.
- Choose the cheapest GPU that fits the VRAM/throughput requirement.
- Name Pods `<person>-<project>-<purpose>`.
- **Attach `spar-super-lab-workspace` for normal experiments that use the shared model pool.**
- Put high-I/O scratch on Pod-local storage.
- Delete Pods when finished.

## Global Volume

The lab volume is `spar-super-lab-workspace`.

Its primary shared role is the model pool:

```text
/workspace/hot-cache/models/
```

See [Shared model pool](model_pool.md).

The Global Volume can also be used for hot/staging data, but it should not be the only copy of unique scientific results.
