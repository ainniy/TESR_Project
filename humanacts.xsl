<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:tei="http://www.tei-c.org/ns/1.0">
    <xsl:template match="/">
        <html> 
            <head>
                <meta charset="UTF-8"/>
                <title>Human Acts</title>
            </head>
            <body>
                <h2>
                    <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
                </h2>
                <xsl:apply-templates select="tei:TEI/tei:text/tei:body"/>
            </body>    
        </html>
    </xsl:template>

    <xsl:template match="tei:div">
        <xsl:apply-templates select="tei:head"/>
        <xsl:apply-templates select="tei:p"/>
    </xsl:template>

    <xsl:template match="tei:head">
        <xsl:choose>
            <xsl:when test="@rend='bold'">
                <h3><strong><xsl:apply-templates/></strong></h3>
            </xsl:when>
            <xsl:otherwise>
                <h3><xsl:apply-templates/></h3>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="tei:p">
        <p><xsl:apply-templates/></p>
    </xsl:template>

    <xsl:template match="tei:q">
        <q><xsl:apply-templates/></q>
    </xsl:template>

    <xsl:template match="tei:hi">
        <i><xsl:apply-templates/></i>
    </xsl:template>

    <xsl:template match="tei:persName">
        <a><xsl:apply-templates/></a>
    </xsl:template>
    <xsl:template match="tei:placeName">
        <a><xsl:apply-templates/></a>
    </xsl:template>


</xsl:stylesheet>