# Backlog

## 1. BunkerWeb reverse proxy
- Deploy BunkerWeb as reverse proxy in front of all services
- Once live, update all `health_check_url` values in `host_vars/` to go through BunkerWeb
- Add BunkerWeb's own host as a priority update target at the start of `vm-updates.yml`, before patching the other VMs

## 2. Weekly VM backup to pCloud
- Every Friday: run `vzdump` for each VM on the Proxmox cluster
- Upload the resulting backup to pCloud via rclone (native pCloud API, consistent with the existing `smb101` backup setup)
- Delete the local vzdump file after a successful upload
- Retention: keep 2 backups on pCloud for now
