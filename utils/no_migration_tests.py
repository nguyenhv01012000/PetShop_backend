import sys

TESTING = "test" in sys.argv[1:]
if TESTING:
    print("=========================")
    print("In TEST Mode - Disableling Migrations")
    print("=========================")

    class DisableMigrations(object):
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = DisableMigrations()