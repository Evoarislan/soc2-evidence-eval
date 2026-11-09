# Backup and Restore Policy (excerpt)

Policy ID: POL-BKP-002 - Effective: 2026-01-15 - Owner: Director of IT Operations

1. Production databases are backed up nightly. Backup job completion is
   monitored, and failed jobs are retried within the same backup window.
2. Backups are retained for 35 days in the backup platform.
3. Restore testing: a full restore of each production database backup
   must be performed and verified at least quarterly. Every restore
   test is documented in a restore test record showing the backup
   restored, the test date, the verification checks performed, and the
   result.
4. The restore test record is the audit evidence of restorability.
   Backup job completion records show that data was copied; they are
   not, on their own, evidence that data can be restored.
