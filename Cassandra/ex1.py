import logging
import time
import msgpack

from cassandra.cluster import Cluster

'''Install Cassandra as here:

https://dzone.com/articles/install-cassandra-on-ubuntu-1804

'''


products = [
    {
        "image_url": "http://a.com",
        "group_id": "1",
        "name": "a",
        "sku": "a-1",
        "url": "http://a.com",
        "description": "line1\nline2",
        "in_stock": "TRUE",
        "price": "1.1",
        "categories": "cat1"
    },
    {
        "image_url": "http://b.com",
        "group_id": "1",
        "name": "b",
        "sku": "b-1",
        "url": "http://b.com",
        "description": "description with, a comma",
        "in_stock": "TRUE",
        "price": "1.2",
        "categories": "cat1"
    },
    {
        "image_url": "http://c.com",
        "group_id": "1",
        "name": "c",
        "sku": "c-1",
        "url": "http://c.com",
        "description": "some description",
        "in_stock": "TRUE",
        "price": "1.3",
        "categories": "cat1"
    },
    {
        "image_url": "http://d.com",
        "group_id": "2",
        "name": "d",
        "sku": "d-2",
        "url": "http://d.com",
        "description": "f",
        "in_stock": "TRUE",
        "price": "1",
        "categories": "cat1|cat2"
    },
    {
        "image_url": "http://e.com",
        "group_id": "2",
        "name": "e",
        "sku": "e-2",
        "url": "http://e.com",
        "description": "",
        "in_stock": "TRUE",
        "price": "3",
        "categories": "cat1|cat2"
    },
    {
        "image_url": "http://f.com",
        "group_id": "2",
        "name": "f",
        "sku": "f-2",
        "url": "http://f.com",
        "description": "f",
        "in_stock": "TRUE",
        "price": "3.4",
        "categories": "cat1|cat2"
    },
    {
        "image_url": "http://g.com",
        "group_id": "3",
        "name": "g",
        "sku": "g-3",
        "url": "http://g.com",
        "description": "",
        "in_stock": "TRUE",
        "price": "1.3455",
        "categories": "cat3"
    },
    {
        "image_url": "http://h.com",
        "group_id": "3",
        "name": "h",
        "sku": "h-3",
        "url": "http://h.com",
        "description": "",
        "in_stock": "TRUE",
        "price": "1234",
        "categories": "cat3"
    },
    {
        "image_url": "http://i.com",
        "group_id": "3",
        "name": "i",
        "sku": "i-3",
        "url": "http://i.com",
        "description": "dafd",
        "in_stock": "TRUE",
        "price": "341",
        "categories": "cat3"
    }
]


def main():

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)

    # log = logging.getLogger()
    # log.setLevel('DEBUG')
    # handler = logging.StreamHandler()
    # handler.setFormatter(logging.Formatter(
    #     "%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    # log.addHandler(handler)

    KEYSPACE = 'deltas'
    TABLE = 'deltas'
    SECTION = 8769541
    FEED = 12113

    cluster = Cluster()
    session = cluster.connect()

    rows = session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
    if KEYSPACE in [row[0] for row in rows]:
        log.info("dropping existing keyspace...")
        session.execute("DROP KEYSPACE " + KEYSPACE)

    log.info("creating keyspace...")
    session.execute("""
            CREATE KEYSPACE IF NOT EXISTS %s
            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '3' }
            """ % KEYSPACE)

    session.set_keyspace(KEYSPACE)

    log.info("creating table %s", TABLE)

    table_query = """
    CREATE TABLE "%s" (
    section_id text,
    feed_id text,
    ts timestamp,
    item_id text,
    action text,
    data blob,
    PRIMARY KEY ((section_id, feed_id), ts)
    )""" % TABLE

    log.debug('running query %s', table_query)
    session.execute(table_query)

    now = int(round(time.time() * 1000))

    log.info("starting from %s", now)

    prepared = session.prepare("""
            INSERT INTO "{}" (section_id, feed_id, ts, item_id, action, data)
            VALUES (?, ?, ?, ?, ?, ?)
            """.format(TABLE))

    for i in range(10000):
        product = products[i % len(products)]
        session.execute(prepared.bind((str(SECTION), str(
            FEED), now + i*1000, product['sku'], "UPSERT", msgpack.packb(product))))

    future = session.execute_async('SELECT * FROM "{}" limit 1'.format(TABLE))
    try:
        rows = future.result()
    except Exception:
        log.exeception()

    log.info("fetching one item from table")
    for row in rows:
        log.info('feed_id={}, ts={}, item_id={}, action={}, data={}'.format(
            row.feed_id, row.ts, row.item_id, row.action, msgpack.unpackb(row.data)))


main()
