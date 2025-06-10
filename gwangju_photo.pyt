import xml.etree.ElementTree as ET
import hashlib
import rdflib
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, XSD, FOAF

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

g.add((metadata_uri, RDF.type, DBO.Photo))
g.add((metadata_uri, RDFS.label, Literal(title_ko, lang="ko")))
g.add((metadata_uri, RDFS.label, Literal(title_en, lang="en")))
g.add((metadata_uri, ex.description_ko, Literal(description_ko, lang="ko")))
g.add((metadata_uri, ex.description_en, Literal(description_en ,lang="en")))
g.add((metadata_uri, ex.photoID, Literal(photoID)))
g.add((metadata_uri, DBO.photographer, Literal(photographer)))
g.add((metadata_uri, ex.webpageURL, Literal(webpageURL)))
g.add((metadata_uri, DBO.date, Literal(date, datatype=XSD.date)))
g.add((metadata_uri, ex.source, Literal(source)))
g.add((metadata_uri, DBO.copyright, Literal(copyright)))

for s,p,o in g.triples((None, None, None)):
    print(s, p, o)

g.serialize(destination="gwangju_photo.ttl", format="turtle")