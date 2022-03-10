from neo4j import GraphDatabase

# Important!!!!!!!!
"""
    For this to work you will need to install neo4j desktop (and the python lib. see req.) which you can find here: 
    https://neo4j.com/download/?ref=get-started-dropdown-cta
    
    You will need to enter the requested information, tho since you don't need to verify the email (at least not when I
    did it) the info can be whatever as long as it is not a 10-Minute-Mail-Address. After that the installer should 
    download. (It might be the wrong one for your OS).
    You will also see a key - save that! - which you will need to enter when installed. The installation should be self-
    explanatory.
    
    Once you're set up create a project and a clean db within it. The name can be whatever but for password set 'kgl' or
    adjust the code according to your choice. Then launch the db. 
    (Note: the demo-db might be running in which case you'll need to terminate it first.)
    
    If you want to see your db visually, select bloom from the "open"-drop-down-menu in the neo4j desktop application.
    
    Also keep in mind that this is the first attempt of integrating neo4j so things might not work as intended and we'll
    need to troubleshoot either on our own or together. 
    
    If you did all that remove the first print and sys.exit() from the main method.
"""


class neo:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self.driver.close()

    # For understanding: if there are no numbers ie.: c1 in the function then it will try to reuse existing nodes
    # The number in the function denotes which node will always be created even if it means duplication

    # Adds a node to the graph if the node does not exist yet
    def add_node(self, content, cat):
        with self.driver.session() as session:
            response = session.write_transaction(self.add_to_graph1, content, cat)
            print(response)

    # Adds a node to the graph even if the node already exists
    def add_node_c1(self, content, cat):
        with self.driver.session() as session:
            response = session.write_transaction(self.add_to_graph11, content, cat)
            print(response)

    # Adds a relation between two nodes to the graph and tries to reuse existing nodes if possible else new are created
    def add_two_nodes(self, content1, cat1, content2, cat2, relation):
        with self.driver.session() as session:
            response = session.write_transaction(self.add_to_graph2, content1, cat1, content2, cat2, relation)
            print(response)

    # Adds a relation between two nodes to the graph will add the first node even if it means duplication and tries
    # to reuse an existing node for the second if possible else a new node is created
    def add_two_nodes_c1(self, content1, cat1, content2, cat2, relation):
        with self.driver.session() as session:
            response = session.write_transaction(self.add_to_graph21, content1, cat1, content2, cat2, relation)
            print(response)

    # Adds a relation between two nodes to the graph will add the second node even if it means duplication and tries
    # to reuse an existing node for the first if possible else a new node is created
    def add_two_nodes_c2(self, content1, cat1, content2, cat2, relation):
        with self.driver.session() as session:
            response = session.write_transaction(self.add_to_graph22, content1, cat1, content2, cat2, relation)
            print(response)

    # Adds a relation between two nodes and will always create new nodes for each even if it means duplication
    def add_two_nodes_c12(self, content1, cat1, content2, cat2, relation):
        with self.driver.session() as session:
            response = session.write_transaction(self.add_to_graph22, content1, cat1, content2, cat2, relation)
            print(response)

    # Adds a relation between two nodes and will always create new nodes for each even if it means duplication
    def add_property(self, node, type, prop, value):
        with self.driver.session() as session:
            response = session.write_transaction(self.add_property_to, node, type, prop, value)
            print(response)

    @staticmethod
    def add_to_graph1(tx, content, cat):
        query = (
            f"MERGE (a:{cat} {{name: $content}}) "
            "RETURN a.message + ', from node ' + id(a)"
        )
        result = tx.run(query, content=content)
        return result.single()[0]


    @staticmethod
    def add_to_graph11(tx, content, cat):
        query = (
            f"CREATE (a:{cat} {{name: $content}}) "
            "RETURN a.message + ', from node ' + id(a)"
        )
        result = tx.run(query, content=content)
        return result.single()[0]


    @staticmethod
    def add_to_graph2(tx, content1, cat1, content2, cat2, relation):
        query = (
            f"MERGE (a:{cat1} {{name: $content1}}) "
            f"MERGE (b:{cat2} {{name: $content2}}) "
            f"MERGE (a)-[:{relation}]->(b)"
            "RETURN a.message + ', from node ' + id(a)"
        )
        result = tx.run(query, content1=content1, content2=content2)
        return result.single()[0]

    @staticmethod
    def add_to_graph21(tx, content1, cat1, content2, cat2, relation):
        query = (
            f"CREATE (a:{cat1} {{name: $content1}}) "
            f"MERGE (b:{cat2} {{name: $content2}}) "
            f"MERGE (a)-[:{relation}]->(b)"
            "RETURN a.message + ', from node ' + id(a)"
        )
        result = tx.run(query, content1=content1, content2=content2)
        return result.single()[0]

    @staticmethod
    def add_to_graph22(tx, content1, cat1, content2, cat2, relation):
        query = (
            f"MERGE (a:{cat1} {{name: $content1}}) "
            f"CREATE (b:{cat2} {{name: $content2}}) "
            f"MERGE (a)-[:{relation}]->(b)"
            "RETURN a.message + ', from node ' + id(a)"
        )
        result = tx.run(query, content1=content1, content2=content2)
        return result.single()[0]


    @staticmethod
    def add_to_graph212(tx, content1, cat1, content2, cat2, relation):
        query = (
            f"CREATE (a:{cat1} {{name: $content}}) "
            f"CREATE (b:{cat2} {{name: $content2}}) "
            f"MERGE (a)-[:{relation}]->(b)"
            "RETURN a.message + ', from node ' + id(a)"
        )
        result = tx.run(query, content1=content1, content2=content2)
        return result.single()[0]


    @staticmethod
    def add_property_to(tx, node, type, prop, value):
        query = (
            f"MATCH (a:{type} {{name: '{node}'}}) "
            f"SET a.{prop} = '{value}'"
            "RETURN a.message + ', from node ' + id(a)"
        )
        result = tx.run(query)
        return result.single()[0]

