from dsltools.processor import Processor

from dsltools.base_item import BaseItem
from xml.etree.ElementTree import ElementTree


class TestItem(BaseItem):
    def __init__(self):
        BaseItem.__init__(self)

class Test:
    def __init__(self, xmlfile):
        self.tree = self.readXML(xmlfile)

    def readXML(self, xmlfile):
        itemroot = TestItem()

        tree = ElementTree(file=open(xmlfile, 'r'))
        root = tree.getroot()
        itemroot.tag = root.tag
        
        for element in root.findall('struct'):
            for item in element.getiterator():
                break
        return itemroot

    def output(self, a, b):
        print a
        print b
        return

def main(generator):
    encode = "utf8"
    prefix = "game_"
    template_dir = "./hoge_tmpl"
    output_dir = "."

    processor = Processor(template_dir, output_dir, prefix, encode)
    processor.proc(generator.output)

xmlfile = "./hoge.xml";
main(Test(xmlfile))
