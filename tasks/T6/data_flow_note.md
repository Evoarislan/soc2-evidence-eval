# Data Flow Note - Production Backups (internal architecture summary)

- System: Copperline production platform
- Prepared by: Platform Engineering, 2026-04-08

Production databases and object storage are backed up nightly to the
VaultKeep managed backup subsystem (backup storage, replication, and
restore services). Backup retention is 35 days. The primary storage
platform holds live data only; all backup copies reside in the managed
backup subsystem.

Restore tests are run quarterly from backups held in that subsystem.
