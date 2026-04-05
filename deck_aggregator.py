from os import listdir
from os.path import isfile, join
from collections import Counter
from pathlib import Path
import sys

base_path_lists = "./lists"
base_path_save = "./results/"

#get all lists

def loadlists(path):
    allContainedcards = []
    cardname_dict = {}
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for f in onlyfiles:
        deck = []
        with open(path+"/"+f, "r", encoding="utf-8") as deck:
            lines = deck.readlines()
            for line in lines[1:]:
                card = line.split(" ")
                cardcode = trim_cardcode_rarity(card[1])
                
                card_code_to_use = cardcode
                if card_code_to_use not in cardname_dict:
                    for key in cardname_dict.keys():
                        if cardname_dict[key] == " ".join(card[2:]).strip():
                            card_code_to_use = key
                    if cardcode == card_code_to_use:
                        cardname_dict[card_code_to_use] = " ".join(card[2:]).strip()
                for _ in range(int(card[0])):
                    allContainedcards.append(card_code_to_use)
    
    return allContainedcards, len(onlyfiles), cardname_dict

def create_agg_list(quantity, cardcodes, cardnames):
    agg_list = []
    for i in range(len(cardcodes)):
        line = str(quantity[i])+" "+str(cardcodes[i])+" "+cardnames[cardcodes[i]]
        agg_list.append(line)
    return agg_list

def print_to_file(list,name):
    with open(base_path_save+name+".txt", 'w', encoding="utf-8") as f:
        for cardLine in list:
            card = cardLine.split(" ")
            f.write(card[0])
            f.write(" ")
            f.write(card[1])
            f.write(" ")
            f.write(" ".join(card[2:]).strip())
            f.write("\n")
    f.close()
    return(base_path_save+"results.txt")

def trim_cardcode_rarity(cardcode):
    while cardcode and not cardcode[-1].isdigit():
        cardcode = cardcode[:-1]
    return cardcode


def main():
    print("Aggregating lists...  ", end="")
    folder_to_use = sys.argv[1] if len(sys.argv) > 1 else base_path_lists
    cards_to_agg, deckcounts, cardname_dict = loadlists(folder_to_use)
    c = Counter(cards_to_agg)
    cards = list(c.keys())
    quantity = list(c.values())
    average_quantity = [round(x/deckcounts,2) for x in quantity]
    final_list = create_agg_list(average_quantity,cards,cardname_dict)
    name = sys.argv[2] if len(sys.argv) > 2 else Path(folder_to_use).stem
    file_path = print_to_file(final_list, name)
    print("Success!")
    print("File can be found in: "+file_path)

main()