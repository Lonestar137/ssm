import xml.etree.ElementTree as ET

def Menu_Heirarchy(database):
    #TODO Make this more efficient.
    #It needs to be dynamic, right now it is static to only a few layers deep.

    for folder in database:
        #print(folder.attrib)
        if folder.attrib['type'] == 'folder':
            for district in folder:
                print('\t',district.attrib['name'])

                if district.attrib['type'] == 'folder':
                    for host in district:
                        print('\t\t', host.attrib['name'])

                        #NOTE Works but adds unnecessary clutter.
                        #for field in host:
                            #Filter unwanted details from the Host
                        #    if field.text not in ['None', None] and field.tag in ['host']:
                                #print('\t\t\t', field.tag+':',field.text)
                        #        print('\t\t\t', field.tag+':',field.text)

        else:
            print('Not in folder ', folder.attrib['name'])

tree = ET.parse('TestDatabase.dat')
root = tree.getroot()

#Generate heirarchy
Menu_Heirarchy(root)
