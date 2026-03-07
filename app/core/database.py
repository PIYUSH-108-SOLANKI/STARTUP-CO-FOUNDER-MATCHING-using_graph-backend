from neo4j import GraphDatabase
from app.core.config import settings


class Neo4jConnection:

    def __init__(self):
        self._connect()

    def _connect(self):
        """
        Creates a fresh connection to Neo4j Aura.
        Called once on startup and again if connection drops.
        
        max_connection_lifetime=200 → don't hold a connection for more than 200s
        keep_alive=True             → send keepalive pings so Aura doesn't pause it
        """
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
            max_connection_lifetime=200,
            keep_alive=True
        )

    def close(self):
        self.driver.close()

    def execute_query(self, query, parameters=None):
        """
        Runs a Cypher query. 
        If the connection is defunct (dropped by Aura free tier timeout),
        it automatically reconnects once and retries.
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters)
                return [record.data() for record in result]

        except Exception as e:
            # "defunct connection" = Neo4j Aura dropped our idle connection
            if "defunct" in str(e).lower():
                print("[DB] Connection was defunct. Reconnecting to Neo4j Aura...")
                self._connect()  # create a fresh connection
                # Retry the query once with the new connection
                with self.driver.session() as session:
                    result = session.run(query, parameters)
                    return [record.data() for record in result]
            # Any other error — raise it so we can see what's wrong
            raise


db = Neo4jConnection()