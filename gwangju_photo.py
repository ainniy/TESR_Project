import xml.etree.ElementTree as ET
import hashlib
import rdflib
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, XSD, DC, FOAF

tree= ET.parse("gwangju_photo.xml")
root=tree.getroot()

g=Graph()
DBO=Namespace("http://dbpedia.org/ontology/")
ex=Namespace("http://w3id.org/example/")

title_ko= root.find("photo/title_ko").text
title_en= root.find("photo/title_en").text
description_ko=root.find("photo/description_ko").text
description_en=root.find("photo/description_en").text
photoID=root.find("photo/photoID").text
photographer=root.find("photo/photographer").text
date=root.find("photo/date").attrib.get("when")
webpageURL=root.find("photo/webpageURL").text
source=root.find("photo/source").text
copyright=root.find("photo/copyright").text

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