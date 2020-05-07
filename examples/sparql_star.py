from rdflib import Graph
from rdflib.namespace import RDF, Namespace
from pyparsing import ParseException

reif_as_object = """
    PREFIX ex:<http://example.org/>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    ex:subject ex:predicate ex:object .
    ex:reif a rdf:Statement ;
     rdf:subject ex:subject ;
     rdf:predicate ex:predicate ;
     rdf:object ex:object .
    ex:about a ex:reif .
    """
reif_as_subject = """
        PREFIX ex:<http://example.org/>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        ex:subject ex:predicate ex:object .
        ex:reif a rdf:Statement ;
         rdf:subject ex:subject ;
         rdf:predicate ex:predicate ;
         rdf:object ex:object .
        ex:reif a ex:about .
        """

def test_basic_sparql_star_subject():
    g = Graph()
    g.parse(data=reif_as_object, format="ttl")
    res = g.query('''SELECT * WHERE {<< ?s ?p ?o >> ?p2 ?o2 . }''')

    rl = list(res)
    print (rl)
    print (len(rl))


def test_basic_sparql_star_object():
    g = Graph()
    g.parse(data=reif_as_object, format="ttl")
    res = g.query('''SELECT * WHERE {
?s ?p << ?s2 ?p2 ?o2 >> . 
}''')
    rl = list(res)
    print(rl)
    print(len(rl))
    #self.assertEqual(1 , len(rl))


def test_basic_sparql():
    g = Graph()
    g.parse(data=reif_as_object, format="ttl")
    res = g.query('''PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    SELECT * WHERE {
    ?s ?p ?o . 
    ?r a rdf:Statement ;
       rdf:subject ?s ;
       rdf:predicate ?p ;
       rdf:object ?o .
    ex:about a ?r.
    }''')
    rl = list(res)
    #self.assertEqual(1 , len(rl))
    print(len(rl))
    print(rl)

def test_bind_sparql_star():
    g = Graph()
    g.parse(data=reif_as_subject, format="ttl")
    res = g.query('''SELECT * WHERE { BIND(<< ?s2 ?p2 ?o2 >> AS ?b) }''')
    rl = list(res)
    #self.assertEqual(1, len(rl))
    print(rl)
    print(len(rl))

def test_constant_sparql_star_object():
    g = Graph()
    g.parse(data=reif_as_subject, format="ttl")
    res = g.query('''PREFIX ex:<http://example.org/> SELECT * WHERE {
    << ex:subject ex:predicate ?object >> a ex:about  . 
    }''')
    rl = list(res)
    #self.assertEqual(1 , len(rl))
    print(rl)
    print(len(rl))

def test_constant_sparql_object():
    g = Graph()
    g.parse(data=reif_as_subject, format="ttl")
    res = g.query('''PREFIX ex:<http://example.org/> SELECT * WHERE {
    ex:subject ex:predicate ?object .
    ex:reif a ex:about  ;
    a rdf:Statement ;
    rdf:subject ex:subject ;
    rdf:predicate ex:predicate ;
    rdf:object ?object . 
    }''')
    rl = list(res)
    #self.assertEqual(1 , len(rl))
    print(rl)
    print(len(rl))

def test_constant_sparql_star_values():
    g = Graph()
    g.parse(data=reif_as_subject, format="ttl")
    res = g.query('''PREFIX ex:<http://example.org/> SELECT * WHERE {
    VALUES(?reif) {(<< ex:subject ex:predicate ex:object>>)}
    ?reif a ex:about  . 
    }''')
    rl = list(res)
    #self.assertEqual(1 , len(rl))
    print(rl)
    print(len(rl))

#This should fail as the embedded triple is not well formed
def test_non_constant_sparql_star_values():
    g = Graph()
    g.parse(data=reif_as_subject, format="ttl")
    #with self.assertRaises(ParseException):
    g.query('''PREFIX ex:<http://example.org/> SELECT * WHERE {
   VALUES(?reif) {(<< ex:subject ex:predicate ?o>>)}
   ?reif a ex:about  . 
   }''')


if __name__ == '__main__':
    test_basic_sparql_star_subject()