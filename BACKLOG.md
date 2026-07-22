# Backlog

## 1. PVE update playbook (CV_Proxmox)
Same logic as `automatic_updates` (Katello promote/publish) but for `CV_Proxmox`, applied to the Proxmox hosts themselves (pve1/pve2/pve3). Must include:
- Content view promote to Production + publish new version + promote to Test (same pattern as CV_Rocky_10)
- Smart VM migration before patching a node: check available resources (CPU/RAM) on the other nodes before migrating
- Reboot the node once VMs are migrated off
- Once all 3 nodes are updated: rebalance VMs back across the 3 hosts

## 2. BunkerWeb reverse proxy
- Deploy BunkerWeb as reverse proxy in front of all services
- Once live, update all `health_check_url` values in `host_vars/` to go through BunkerWeb
- Add BunkerWeb's own host as a priority update target at the start of `automatic_updates`, before patching the other VMs

## 3. Weekly VM backup to pCloud
- Every Friday: run `vzdump` for each VM on the Proxmox cluster
- Upload the resulting backup to pCloud via rclone (native pCloud API, consistent with the existing `smb101` backup setup)
- Delete the local vzdump file after a successful upload
- Retention: keep 2 backups on pCloud for now
