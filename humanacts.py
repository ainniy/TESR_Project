import xml.etree.ElementTree as ET
import hashlib
import rdflib
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, XSD, FOAF, DC

tree= ET.parse("humanacts.xml")
root=tree.getroot()
ns={"tei":"http://www.tei-c.org/ns/1.0"}

g=Graph()
DBO=Namespace("http://dbpedia.org/ontology/")
schema= Namespace("http://schema.org/")
ex=Namespace("http://w3id.org/example/")

title= root.find(".//tei:titleStmt/tei:title", ns).text
editor=root.find(".//tei:respStmt/tei:resp", ns).text+ ":"+ root.find(".//tei:respStmt/tei:name", ns).text
source_author=root.find("tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:author", ns).text
source_translator=root.find("tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:translator", ns).text
source_title=root.find("tei:teiHeader/tei:fileDesc/tei:sourceDesc//tei:bibl/tei:title", ns).text
source_date=root.find("tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:date", ns).attrib.get("when")


book_id=hashlib.md5(title.encode("utf-8")).hexdigest()
book_uri= URIRef(ex+book_id)

editor_id=hashlib.md5(editor.encode("utf-8")).hexdigest()
editor_uri=URIRef(ex+editor_id)
g.add((editor_uri, RDF.type, FOAF.Person))
g.add((editor_uri, FOAF.name, Literal(editor)))

source_author_id=hashlib.md5(source_author.encode("utf-8")).hexdigest()
source_author_uri=URIRef(ex+source_author_id)
g.add((source_author_uri, RDF.type, FOAF.Person))
g.add((source_author_uri, FOAF.name, Literal(source_author)))

source_translator_id=hashlib.md5(source_translator.encode("utf-8")).hexdigest()
source_translator_uri=URIRef(ex+source_translator_id)
g.add((source_translator_uri, RDF.type, FOAF.Person))
g.add((source_translator_uri, FOAF.name, Literal(source_translator)))



g.add((book_uri, RDF.type, DBO.Book))
g.add((book_uri, RDFS.label, Literal(title)))
g.add((book_uri, DBO.editor, editor_uri))
g.add((book_uri, DBO.author, source_author_uri))
g.add((book_uri, DBO.translator, source_translator_uri))
g.add((book_uri, DBO.publicationDate, Literal(source_date, datatype=XSD.gYear)))

#등장하는 장소
places={}
for place in root.findall(".//tei:teiHeader/profileDesc/listPlace/tei:place", ns):
    place_name=place.findtext("tei:placeName", namespaces=ns)
    if place_name:
        place_id= hashlib.md5(place_name.encode("utf-8")).hexdigest()
        place_uri = URIRef(ex+place_id)
        places[place_name]=place_uri

for place_name, place_uri in places.items():
    g.add((place_uri, RDF.type, DBO.Place))
    g.add((place_uri, RDFS.label, Literal(place_name)))
    g.add((book_uri, schema.locationCreated, place_uri))

#등장하는 사람
people={}

for person in root.findall(".//tei:listPerson/tei:person", ns):
    real_name=""
    fiction_name=""
    default_name=""

    for persName in person.findall("tei:persName",ns):
        name_type=persName.attrib.get("type", "")
        if name_type == "real":
            real_name= persName.text
        elif name_type == "fiction":
            fiction_name= persName.text
        else:
            default_name= persName.text

    person_name=default_name or fiction_name
    person_id= hashlib.md5(person_name.encode("utf-8")).hexdigest()
    person_uri= URIRef(ex+person_id)
    people[person_name]=person_uri

    if real_name:
        g.add((person_uri, FOAF.name, Literal(real_name)))

for person_name, person_uri in people.items():
    g.add((person_uri, RDF.type, FOAF.Person))
    g.add((person_uri, RDFS.label, Literal(person_name)))
    g.add((book_uri, schema.character, person_uri))



events={}
for event in root.findall(".//tei:teiHeader/profileDesc/listEvent/tei:event", ns):
    event_name=event.findtext("tei:desc", namespaces=ns)
    event_date=event.attrib.get("when")
    if event_name:
        event_id= hashlib.md5(event_name.encode("utf-8")).hexdigest()
        event_uri= URIRef(ex+event_id)
        events[event_name]=(event_uri, event_date)
        
for event_name, (event_uri, event_date) in events.items():
    g.add((event_uri, RDF.type, DBO.Event))
    g.add((event_uri, RDFS.label, Literal(event_name)))
    g.add((event_uri, DC.date, Literal(event_date, datatype=XSD.date)))
    g.add((book_uri, schema.event, event_uri)) 

related_item=root.find(".//tei:relatedItem", ns)
if related_item:
    target_filename= related_item.attrib.get("target")
    if target_filename:
        photo_background_id=hashlib.md5(target_filename.encode("utf-8")).hexdigest()
        photo_background_uri=URIRef(ex+photo_background_id)
        g.add((photo_background_uri, RDF.type, schema.ImageObject))
        g.add((photo_background_uri, RDFS.label, Literal(f"Background photos from {target_filename}")))
        g.add((book_uri, schema.associatedMedia, photo_background_uri))




for s,p,o in g.triples((None, None, None)):
    print(s, p, o)

g.serialize(destination="humanacts.ttl", format="turtle")