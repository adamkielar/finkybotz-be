CLEAR_DB_SQL = """
    -- Disconect all constraints from all tables --
    EXEC sp_MSForEachTable "ALTER TABLE ? NOCHECK CONSTRAINT all",
    @whereand='and o.Name not like ''%alembic_version%'''
    -- Clear all tables except alembic_version table --
    EXEC sp_MSForEachTable "DELETE FROM ?",
    @whereand='and o.Name not like ''%alembic_version%'''
    -- Reconnect constraints back --
    EXEC sp_MSForEachTable "ALTER TABLE ? WITH CHECK CHECK CONSTRAINT all",
    @whereand='and o.Name not like ''%alembic_version%'''
    -- Reset idendity columns --
    EXEC sp_MSForEachTable "DBCC CHECKIDENT ( '?', RESEED, 0)",
    @whereand='and o.Name != ''alembic_version'' and o.Name != ''client'''
 """
