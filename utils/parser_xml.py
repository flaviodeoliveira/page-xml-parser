import xml.etree.ElementTree as ET

class XmlParser:
    def __init__(self, page_xml="./page_xml.xml"):
        self.tree = ET.parse(page_xml, parser=ET.XMLParser(encoding="utf-8"))
        self.root = self.tree.getroot()
        self.namespace = "{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}"

    # Ensure that the code only tries to access the <Unicode> child element if the <TextEquiv> element exists.
    def xml_to_txt(self, output_file="page_txt.txt"):
        with open(output_file, "w", encoding="utf-8") as f:
            for textregion in self.root.findall(f".//{self.namespace}TextRegion"):
                for textline in textregion.findall(f".//{self.namespace}TextLine"):
                    text_equiv_element = textline.find(f"{self.namespace}TextEquiv")
                    if text_equiv_element is not None:  # Check if <TextEquiv> element exists
                        text = text_equiv_element.find(f"{self.namespace}Unicode").text
                        f.write(text + "\n")
                f.write("\n")

    def extract_texts_and_coords(self):
        texts_coords_list = []
        for textregion in self.root.findall(f".//{self.namespace}TextRegion"):
            for textline in textregion.findall(f".//{self.namespace}TextLine"):
                text_equiv_element = textline.find(f"{self.namespace}TextEquiv")
                if text_equiv_element is not None:  # Check if <TextEquiv> element exists
                    text = text_equiv_element.find(f"{self.namespace}Unicode").text
                    
                    # Extract coordinates
                    coords = textline.find(f"{self.namespace}Coords").attrib["points"].split()
                    points = [tuple(map(int, point.split(","))) for point in coords]
                    texts_coords_list.append((text, points))
        return texts_coords_list

if __name__ == "__main__":
    pass
