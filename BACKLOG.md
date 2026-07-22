# Backlog

## 1. PVE update playbook (CV_Proxmox)
Same logic as `automatic_updates` (Katello promote/publish) but for `CV_Proxmox`, applied to the Proxmox hosts themselves (pve1/pve2/pve3). Must include:
- Content view promote to Production + publish new version + promote to Test (same pattern as CV_Rocky_10)
- Smart VM migration before patching a node: check available resources (CPU/RAM) on the other nodes before migrating
- Reboot the node once VMs are migrated off
- Once all 3 nodes are updated: rebalance VMs back across the 3 hosts

## 2. Podman container update playbook (DONE)
Implemented as `container-updates.yml`, validated end-to-end on adguard101, patchmon101, phpipam101, and immich101.
- Snapshot (ansible_container) before update
- Pull latest image, restart Quadlet unit only if image changed (idempotent)
- Health check after update
- Image retention: keep last 2 per repository
- Supports root scope, rootless (same user), and rootless cross-user (become_user) via host_vars podman_units

## 3. BunkerWeb reverse proxy
- Deploy BunkerWeb as reverse proxy in front of all services
- Once live, update all `health_check_url` values in `host_vars/` to go through BunkerWeb
- Add BunkerWeb's own host as a priority update target at the start of `automatic_updates`, before patching the other VMs

## 4. Weekly VM backup to pCloud
- Every Friday: run `vzdump` for each VM on the Proxmox cluster
- Upload the resulting backup to pCloud via rclone (native pCloud API, consistent with the existing `smb101` backup setup)
- Delete the local vzdump file after a successful upload
- Retention: keep 2 backups on pCloud for now

## 5. Content view version retention playbook
Automatic cleanup of old content view versions to prevent unbounded growth from weekly publishes.
- Applies to both `CV_Rocky_10` and `CV_Proxmox`
- Retention: keep the last 10 versions per content view, delete older ones

## 6. Schedule cleanup-container-snapshots
The `cleanup-container-snapshots.yml` playbook exists but has no schedule yet.
- Scheduling frequency: TBD (depends on how often `container-updates` ends up running)
