This project involves transforming metadata from the novel "Human Acts" (in XML format) and related Gwangju photographs (in a separate XML file) into RDF (Resource Description Framework) format. The goal is to semantically connect these two datasets and build a knowledge graph that can be utilized on the web.

humanacts.xml: TEI XML metadata for the novel "Human Acts."
gwangju_photo.xml: TEI XML metadata for the Gwangju photographs.

humanacts.py: Python script to parse humanacts.xml and generate humanacts.ttl.
gwangju_photo.py: Python script to parse gwangju_photo.xml and generate gwangju_photo.ttl.

humanacts.ttl: Generated RDF data for the novel.
gwangju_photo.ttl: Generated RDF data for the Gwangju photographs.

humanacts.xsl: XSLT stylesheet for transforming humanacts.xml into a web page.
humanacts.html: HTML web page result of humanacts.xml transformed by humanacts.xsl.
