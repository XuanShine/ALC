from peewee_migrate import Router
from peewee import SqliteDatabase

router = Router(SqliteDatabase('local.db'))

# Create migration
# router.create('migration002')

# Run migration/migrations
router.run('migration_name')

# Run all unapplied migrations
# router.run()