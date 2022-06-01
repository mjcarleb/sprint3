import pathlib
import xml.dom.minidom

def traverse_and_fix(node):

    try:
        isExec = node.attributes['isExecutable']
        if isExec != "true":
            node.attributes['isExecutable'] = "true"
    except (TypeError, KeyError):
        pass

    children = node.childNodes
    if len(children) == 0:
        if node.localName is not None and "signavio" in node.localName:
            node.parentNode.removeChild(node)
    else:
        for child in children:
            traverse_and_fix(node=child)

in_xml = "process_models/sprint3-process.bpmn"
suffix = pathlib.Path(in_xml).suffix
out_xml = f"{in_xml[:len(in_xml)-len(suffix)]}_C8{suffix}"

domtree = xml.dom.minidom.parse(in_xml)
root = domtree.documentElement


traverse_and_fix(node=root)

domtree.writexml(open(out_xml, "w"), encoding="UTF-8")