class DatabaseRouter:
    """
    A router to control all database operations for different databases
    
    Useful for more complex setups with multiple databases
    """
    def db_for_read(self, model, **hints):
        """
        Suggest the database for reading a particular model
        """
        # Add custom routing logic if needed
        return None

    def db_for_write(self, model, **hints):
        """
        Suggest the database for writing a particular model
        """
        # Add custom routing logic if needed
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations between objects
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Control migration operations
        """
        return True


class PrimaryReplicaRouter:
    """
    A router that sends reads to replicas and writes to the primary database.
    
    This assumes you've configured a database called 'primary' and one or more
    databases with names starting with 'replica'.
    """
    def db_for_read(self, model, **hints):
        """
        Send read operations to replica databases in round-robin fashion.
        """
        import random
        from django.conf import settings
        
        replica_dbs = [db for db in settings.DATABASES if db.startswith('replica')]
        
        if replica_dbs:
            return random.choice(replica_dbs)
        return 'primary'

    def db_for_write(self, model, **hints):
        """
        Send all write operations to the primary.
        """
        return 'primary'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both objects are in the primary/replica dbs.
        """
        db_list = ('primary', *[db for db in settings.DATABASES if db.startswith('replica')])
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Only run migrations on the primary database.
        """
        return db == 'primary'
