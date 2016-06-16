import xmltodict
import  xml.etree.cElementTree as ET
import  pdb
filename=r"D:\Temp\S3temp\common-ios\rootConfig.xml"
pdb.set_trace()
tree=ET.ElementTree(file=filename)
root=tree.getroot()
print root.tag,root.attrib

for child_of_root in root:
    print child_of_root.tag,child_of_root.text


for elem in tree.iter():
    print elem.tag,elem.text


#
# with open(filename,'r') as fd:
#     doc=xmltodict.parse(fd.read())
#
# print doc["Config"]["serverUrl"]

import qiniu
