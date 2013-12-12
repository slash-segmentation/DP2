# http://www.postneo.com/projects/pyxml/

from xml.dom.minidom import Document

# Create the minidom document
doc = Document()

# Create the <wml> base element
object = doc.createElement("object")
object.setAttribute("identifier", "object1")
object.setAttribute("class", "Vesicle")

doc.appendChild(object)

# Create the main <card> element
maincard = doc.createElement("card")
maincard.setAttribute("id", "main")

# Create a <p> element
paragraph1 = doc.createElement("voxels")
object.appendChild(paragraph1)

# Give the <p> elemenet some text
ptext = doc.createTextNode("0,0,0 0,0,0")
paragraph1.appendChild(ptext)

# Print our newly created XML
print doc.toprettyxml(indent="  ")

