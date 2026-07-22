# Backlog

## 1. PVE update playbook (CV_Proxmox)
Same logic as `automatic_updates` (Katello promote/publish) but for `CV_Proxmox`, applied to the Proxmox hosts themselves (pve1/pve2/pve3). Must include:
- Content view promote to Production + publish new version + promote to Test (same pattern as CV_Rocky_10)
- Smart VM migration before patching a node: check available resources (CPU/RAM) on the other nodes before migrating
- Reboot the node once VMs are migrated off
- Once all 3 nodes are updated: rebalance VMs back across the 3 hosts

## 2. Snapshot cleanup playbook
Remove `ansible_patching` snapshots (created by `automatic_updates`) across all VMs.
- Schedule: every Saturday

## 3. Podman container update playbook
Prerequisite: harmonize all container deployments to Quadlet across hosts (adguard101, phpipam101, immich101, patchmon101), for a clean, uniform setup before automating updates.

Once harmonized, for all servers running Podman services via Quadlet:
- Check for new images available for currently running containers (always pull, let Podman/redeploy decide if anything changed)
- Pull new images
- Restart the Quadlet-managed services to pick up new images
- Run health checks after redeployment
- Snapshot before applying changes (cleanup handled by the Saturday snapshot-cleanup job, see #2)
- Image retention: keep the last 2 images per container to allow rollback, prune older ones to avoid unbounded image storage growth

## 4. BunkerWeb reverse proxy
- Deploy BunkerWeb as reverse proxy in front of all services
- Once live, update all `health_check_url` values in `host_vars/` to go through BunkerWeb
- Add BunkerWeb's own host as a priority update target at the start of `automatic_updates`, before patching the other VMs

## 5. Weekly VM backup to pCloud
- Every Friday: run `vzdump` for each VM on the Proxmox cluster
- Upload the resulting backup to pCloud via rclone (native pCloud API, consistent with the existing `smb101` backup setup)
- Delete the local vzdump file after a successful upload
- Retention: keep 2 backups on pCloud for now

## 6. Content view version retention playbook
Automatic cleanup of old content view versions to prevent unbounded growth from weekly publishes.
- Applies to both `CV_Rocky_10` and `CV_Proxmox`
- Retention: keep the last 10 versions per content view, delete older ones
