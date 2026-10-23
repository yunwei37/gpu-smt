# First finite provider start — invalid startup, no GPU verification

Job030754c7-8993-42ee-a479-ec53c29c97ed was assigned to lab. Default
kubectl wait30s expired while the immutable4.66GB image was ContainerCreating.
Kubelet events subsequently show79.083s image pull, container creation/start,
then deletion already requested by cleanup. No native GPU cell started; no
speedup or GPU numerical failure is inferred. Original JobUID/lifecycle,
log and exact script are preserved. No otherWorkspace or node was restarted.
Forward repair follows actual Pod/container condition without an arbitrary
short PodReady deadline and waits for UID-owned Pod deletion; same image/
CUDA library/algorithm/affinity/native24/48GiB settings retained.
