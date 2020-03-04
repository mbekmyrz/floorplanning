import xml.etree.ElementTree as ET


def text_to_xml(txt_file, xml_file):
    file = open(txt_file)
    content = file.read().split()
    rows = content[1]
    columns = content[3]

    tree = ET.parse(xml_file)
    root = tree.getroot()
    root.find('rows').text = rows
    root.find('columns').text = str(len(columns))

    clb_amount = 0
    clb_arrangement = ''
    dsp_amount = 0
    dsp_arrangement = ''
    bram_amount = 0
    bram_arrangement = ''

    for i in range(len(columns)):
        if columns[i] == 'C':
            clb_amount += 1
            clb_arrangement += str(i) + ','
        elif columns[i] == 'D':
            dsp_amount += 1
            dsp_arrangement += str(i) + ','
        elif columns[i] == 'B':
            bram_amount += 1
            bram_arrangement += str(i) + ','
    clb_amount *= int(rows)
    dsp_amount *= int(rows)
    bram_amount *= int(rows)
    clb_arrangement = clb_arrangement[: -1]
    dsp_arrangement = dsp_arrangement[: -1]
    bram_arrangement = bram_arrangement[: -1]

    root.find('./resources/resource[@type = "CLB"]/amount').text = str(clb_amount)
    root.find('./resources/resource[@type = "CLB"]/arrangement').text = clb_arrangement
    root.find('./resources/resource[@type = "DSP"]/amount').text = str(dsp_amount)
    root.find('./resources/resource[@type = "DSP"]/arrangement').text = dsp_arrangement
    root.find('./resources/resource[@type = "BRAM"]/amount').text = str(bram_amount)
    root.find('./resources/resource[@type = "BRAM"]/arrangement').text = bram_arrangement

    tree.write(xml_file)


text_to_xml('fpgaArch.txt', 'description.xml')
