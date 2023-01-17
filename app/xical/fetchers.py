from app.database.postgres.main import psql_cru


def fetch_technical_table():
    psql_cru.execute("select * from technical_table where last_update=(select max(last_update) from technical_table)")
    db_version = psql_cru.fetchone()
    # print(f'fetch_technical_table={db_version}')
    return f'fetch_technical_table={db_version}'


fetch_technical_table()


def fetch_price_history():
    psql_cru.execute("select distinct symbol_id from price_history")
    db_version = psql_cru.fetchone()
    # print(f'fetch_price_historyistory={db_version}')
    return f'fetch_price_history={db_version}'


fetch_price_history()


def fetch_price_history_symbol():
    psql_cru.execute("select * from price_history where symbol_id = {} order by date desc".format('symbol_id'))
    db_version = psql_cru.fetchone()
    # print(f'fetch_price_history_symboltory_symbol={db_version}')
    return f'fetch_price_history_symbol={db_version}'


fetch_price_history_symbol()


def fetch_meta_data_symbol():
    psql_cru.execute("select * from meta_data where symbol_id = {}".format('symbol_id'))
    db_version = psql_cru.fetchone()
    # print(f'meta_data_symbol={db_version}')
    return f'meta_data_symbol={db_version}'


fetch_meta_data_symbol()


def fetch_all_tick_distinct():
    psql_cru.execute("select distinct (symbol_id), symbol from all_tick;")
    db_version = psql_cru.fetchone()
    # print(f'all_tick_distinct={db_version}')
    return f'all_tick_distinct={db_version}'


fetch_all_tick_distinct()


