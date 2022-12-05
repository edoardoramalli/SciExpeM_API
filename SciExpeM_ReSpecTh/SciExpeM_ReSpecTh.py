import xml.etree.ElementTree as ET

root = ET.Element('experiment')

file_author = 'Politecnico di Milano, Italy'
file_doi = '10.5281/zenodo'

# FILE AUTHOR

file_author_element = ET.Element('fileAuthor')
file_author_element.text = file_author
root.append(file_author_element)

# FILE DOI

file_doi_element = ET.Element('fileDOI')
file_doi_element.text = file_doi
root.append(file_doi_element)


ET.indent(root, space="\t", level=0)
tree = ET.tostring(root, encoding='utf-8')
print(tree.decode("utf-8"))