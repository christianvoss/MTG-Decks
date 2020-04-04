import argparse
import re
import xml.etree.ElementTree as xml
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = xml.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def main():
    ##-----------------------------------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description='Get Summary of precious Files for a given Storage Group')
    parser.add_argument('-f', '--forge', help='', type=str)
    parser.add_argument('-c', '--cockatrice', help='', type=str)
    args = parser.parse_args()
    ##-----------------------------------------------------------------------------------------------------

    infile = open(args.forge)

    read_deck = []
    for line in infile:
        read_deck.append(line.strip('\n'))

    deck = list(filter(None, read_deck))
    for line in deck :
        if 'Name=' in line :
            deckname = line.split('=')[1]

    main_deck_list = deck[deck.index('[Main]')+1:deck.index('[Sideboard]')]

    main_board = []
    for card in main_deck_list :
        number = ''.join( re.findall(r'\d+\.?\d*', card.split('|')[0] ) )
        name = [i for i in card.split('|')[0] if not i.isdigit()]
        name.pop(0)
        name_str   = ''.join( name )

        main_board.append( {'number' : number, 'name' : name_str} )

    filename = 'Casual Grixis Swans Possession.cod'

    root = xml.Element("cockatrice_deck")
    deck_name = xml.SubElement(root,"deckname")
    deck_name.text = deckname
    comments = xml.SubElement(root,"comments")
    comments.text = "Converted from Forge"
    zone = xml.SubElement(root,"zone")
    zone.set('name','main')
    for card in main_board :
        card_entry = xml.SubElement(zone, "card")
        card_entry.set('number', card['number'])
        card_entry.set('name', card['name'])

    output_file = open( args.cockatrice, 'w' )
    output_file.write( prettify(root))
    output_file.close()

if __name__== "__main__":
  main()