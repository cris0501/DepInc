# Global database driver for the ORM plugin.
# Each driver lives in depinc/plugins/orm/drivers/<driver>.py — adding a new
# backend (mysql, mongo, redis...) is just dropping a file there.
#
# Override precedence (most specific wins):
#   model._repository  >  service._bindings  >  resolve(overrides)  >
#   config/bindings.py >  this file

database = {
    "driver": "sqlite",        # or "memory"
    "database": "database.db",
}
