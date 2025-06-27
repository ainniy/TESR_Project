import xml.etree.ElementTree as ET
import hashlib
import rdflib
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, XSD, DC, FOAF

tree= ET.parse("gwangju_photo.xml")
root=tree.getroot()

ns={"tei":"http://www.tei-c.org/ns/1.0", "xml":"http://www.w3.org/XML/1998/namespace"}

g=Graph()
DBO=Namespace("http://dbpedia.org/ontology/")
ex=Namespace("http://w3id.org/example/")

title_ko= root.find("tei:figDesc[@xml:lang='ko']", ns).text
title_en= root.find("tei:figDesc[@xml:lang='en']", ns).text
description_ko=root.find("tei:head[@xml:lang='ko']", ns).text
description_en=root.find("tei:head[@xml:lang='en']", ns).text
photoID=root.find("tei:idno[@type='photoID']", ns).text
photographer=root.find("tei:author", ns).text
date=root.find("tei:date", ns).attrib.get("when")
webpageURL=root.find("tei:graphic", ns).attrib.get("url")
source=root.find("tei:source", ns).text
copyright=root.find("tei:availability", ns).text

metadata_id=hashlib.md5(title_en.encode("utf-8")).hexdigest()
metadata_uri= URIRef(ex+metadata_id)

photographer_id=hashlib.md5(photographer.encode("utf-8")).hexdigest()
photographer_uri=URIRef(ex+photographer_id)

g.add((metadata_uri, RDF.type, DBO.Image))
g.add((metadata_uri, RDFS.label, Literal(title_ko, lang="ko")))
g.add((metadata_uri, RDFS.label, Literal(title_en, lang="en")))
g.add((metadata_uri, DC.description, Literal(description_ko, lang="ko")))
g.add((metadata_uri, DC.description, Literal(description_en ,lang="en")))
g.add((metadata_uri, DC.identifier, Literal(photoID)))
g.add((photographer_uri, RDF.type, FOAF.Person))
g.add((photographer_uri, FOAF.name, Literal(photographer)))
g.add((metadata_uri, DBO.photographer, photographer_uri))
g.add((metadata_uri, FOAF.homepage, URIRef(webpageURL)))
g.add((metadata_uri, DC.date, Literal(date, datatype=XSD.date)))
g.add((metadata_uri, DC.source, Literal(source)))
g.add((metadata_uri, DBO.copyright, Literal(copyright)))

for s,p,o in g.triples((None, None, None)):
    print(s, p, o)

g.serialize(destination="gwangju_photo.ttl", format="turtle")