# Encryption-at-Rest Configuration Report

- Generated: 2026-08-19
- Scope: all production data stores, Copperline Systems, Inc.
- Source: cloud configuration export (storage and database services)

## Configuration summary

| Data store            | Encryption at rest | Algorithm | Key management        |
|-----------------------|--------------------|-----------|-----------------------|
| prod-db-primary       | Enabled            | AES-256   | KMS (managed)         |
| prod-db-replica       | Enabled            | AES-256   | KMS (managed)         |
| object-storage-main   | Enabled            | AES-256   | KMS (managed)         |
| object-storage-backup | Enabled            | AES-256   | KMS (managed)         |
| analytics-warehouse   | Enabled            | AES-256   | KMS (managed)         |
| search-index-prod     | Enabled            | AES-256   | KMS (managed)         |

## Key management

- All keys are held in the managed KMS; no keys stored alongside data.
- Automatic key rotation: enabled, 365-day rotation period.
- Last rotation completed: 2026-02-11 (all six stores).
- Key access is restricted to the storage service role; key usage is
  written to the key-access audit trail.

## Exceptions

None. Every production data store reports encryption at rest enabled
with AES-256 and centrally managed keys.
