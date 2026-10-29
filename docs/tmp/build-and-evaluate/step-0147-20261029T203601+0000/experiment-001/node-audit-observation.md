# Read-only node audit — no security change
Existing inventory-derived G10 SSH queried kernel AppArmor signal denials.
The returned matching Python records were:
Oct29 13:00:43 audit(1793304043.559:8516027),profile=cri-containerd.apparmor.d,
pid683 comm=python3 denied send signal=kill peer=cri-containerd.apparmor.d//&unconfined.
Oct29 13:00:43 audit(1793304043.559:8516026),same fields,signal=term.
Other returned records concern coder signal=urg.
These confirm background signal denials against stacked profiles on the node,
but do not independently map hostPID683 to our later namespaced short control.
Do not claim the exact cause of our errno13 is fully localized by these records.
Own control outcome is directly observed TERM/KILL denial and natural retirement.
No AppArmor,permission,container,template,scheduling or other Workspace change.
