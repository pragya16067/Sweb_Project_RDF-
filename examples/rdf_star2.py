from rdflib import Graph
from rdflib.namespace import RDF, Namespace
from pyparsing import ParseException

# For graphs with multiple rdf reification/* statements

rdf_graph = """
    PREFIX ex:<http://example.org/>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf:<http://xmlns.com/foaf/0.1/>
    PREFIX dct:<http://purl.org/dc/terms/>

    ex:bob foaf:name "Bob" ;
            foaf:age 23 .
    _:s rdf:type rdf:Statement ;
    rdf:subject ex:bob ;
    rdf:predicate foaf:age ;
    rdf:object 23 .
    
    _:s2 rdf:type rdf:Statement ;
    rdf:subject ex:bob ;
    rdf:predicate foaf:name ;
    rdf:object "Bob" .
    
    _:s2 foaf:relatedTo _:s .

    _:s dct:creator <http://example.com/crawlers#c1> ;
        dct:source <http://example.net/listing.html> .

    ex:welles foaf:name "John Welles" ;
                ex:mentioned ex:kubrick .
    ex:kubrick foaf:name "Stanley Kubrick" ;
                ex:influencedBy ex:welles .
    _:s1 rdf:type rdf:Statement ;
    rdf:subject ex:kubrick ;
    rdf:predicate ex:influencedBy ;
    rdf:object ex:welles .

    _:s1 dct:creator <http://example.com/names#examples> ;
        dct:source <http://example.net/people.html> .

    """

sparql_query = """
    PREFIX ex:<http://example.org/>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf:<http://xmlns.com/foaf/0.1/>
    PREFIX dct:<http://purl.org/dc/terms/>

    SELECT ?x ?y ?name ?age WHERE {
    ?x foaf:age ?age .
    ?r rdf:type rdf:Statement ;
    rdf:subject ?x ;
    rdf:predicate foaf:age ;
    rdf:object ?age ;
    dct:source ?src . 
    
    ?y foaf:name ?name .
    ?r2 rdf:type rdf:Statement ;
    rdf:subject ?x ;
    rdf:predicate foaf:name ;
    rdf:object ?name .
    }
"""

rdf_Star_graph = """
    PREFIX ex:<http://example.org/>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf:<http://xmlns.com/foaf/0.1/>
    PREFIX dct:<http://purl.org/dc/terms/>

    <<ex:bob foaf:age 23>> foaf:relatedTo <<ex:bob foaf:name "Bob">> ;
    dct:creator <http://example.com/crawlers#c1> ;
    dct:source <http://example.net/listing.html> .

    ex:welles foaf:name "John Welles" ;
                ex:mentioned ex:kubrick .
    ex:kubrick foaf:name "Stanley Kubrick" .
    <<ex:kubrick ex:influencedBy ex:welles>> dct:creator <http://example.com/names#examples> ;
    dct:source <http://example.net/people.html> .

"""

sparql_star_query = """
    PREFIX ex:<http://example.org/>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf:<http://xmlns.com/foaf/0.1/>
    PREFIX dct:<http://purl.org/dc/terms/>

    SELECT ?x ?y ?name ?age WHERE 
    { <<?x foaf:age ?age>> foaf:relatedTo <<?y foaf:name ?name>> .}

"""


def test_rdf_basic():
    g = Graph()
    g.parse(data=rdf_graph, format="turtle")

    for row in g.query(sparql_query):
        print(row)


def test_rdf_star():
    g = Graph()
    g.parse(data=rdf_Star_graph, format="turtle")

    for row in g.query(sparql_query):
        print(row)


if __name__ == '__main__':
    test_rdf_basic()
    test_rdf_star()