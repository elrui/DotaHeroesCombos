import pandas as pd
import csv
import timeit

from ast import literal_eval

FILENAME = 'DataHeroes.xlsx'        # filename for the input datafile
INTERVAL = 1                        # interval in seconds to consider a combo
OUTPUT   = 'CombosDetected.csv'     # output file


def load_file(filename, cleanup=True):
    '''
    This function loads a Pandas Dataframe from the Excel input file
    if cleanup is true, it will delete any irrelevant row with no Item or Ability used
    INPUT:
        filename: Name of the input file
        cleanup:  Wether to clean empty entries or not
    OUTPUT:
        Dataframe containing all the loaded entries
    '''

    df = pd.read_excel(filename) 

    #drop rows with empty items and abilities, if enabled
    if (cleanup):
        df.dropna(axis='index', how='all', subset=['Item', 'Ability'], inplace=True)

    return df


def create_set(listdict, field):
    '''
    This function creates a set of items or abilities (according to the second parameter), eliminating duplicates
    (i.e. this assumes an item/ability cannot appear twice with the same timestamp for the same Hero)
    INPUT:
        listdict: a list of dictionary structures containing the item/ability and timestampo
        field: specifies the field name (item/ability)
    OUTPUT: 
        a ser containing 2-tuples with elements and timestamps
    '''

    newset = set()
    for dict in listdict:
        element = dict[field]
        timex = dict['time']
        if (element!='null'):           # exclude elements called null
            newset.add((element,timex))
    return newset


def create_dictionary(heroeslist, ordered=True):

    '''
    This function creates a dictionary structure with all the abilities and items used by the hero

    INPUT:
        heroeslist: this is an array (matrix) containing all the heroes with their abilities and items used
        ordered: if True will sort the output by timestamp. True is the default value
    OUTPUT: 
        Ductionary with heroes and a list of abilities and items used for each one
    '''

    # Create the return dictionary for a hero
    heroesdict = {}

    for hero in heroeslist:
        
        heroname      = hero[0]
        heroitems     = literal_eval(hero[1])
        # print(heroname)
        # print(hero[2])
        heroabilities = literal_eval(hero[2].replace('null', '"null"'))      # deal with eventual null values, should be fixed on source file

        # Creates the set of all items for the hero
        itemset   = create_set(heroitems, 'item') 

        # Creates the set of all abilities for the hero
        abilityset = create_set(heroabilities, 'ability')
        
        # The complete inventory for the hero includes both sets created above
        heroinventory = itemset.union(abilityset)

        # If we already had an entry for this hero, just update it. If not, add the entry
        if (heroname in heroesdict):
            heroesdict[heroname].update(heroinventory) 
        else:
            heroesdict[heroname] = heroinventory

    # Convert the complete inventory of each hero to a list. If ordered is True, order the list by time
    for k, v in heroesdict.items():
        if (ordered):
            heroesdict[k] = sorted(list(v), key=lambda x: x[1])
        else: 
            heroesdict[k] = list(v)

    return heroesdict

def create_combos(values, interval):
    '''
    This function takes an ordered list of items and abilities and a specified time interval and creates combos
    A combo is defined as a succession of use of two or more combinations of items/abilities in a given timeframe
    INPUT:
        values: the list of items and abilities. Each element is a 2-tuple with the name of the item/ability and timestamp
        interval: time interval to consider a succession is part of a combo
    OUTPUT:
        a list of combos, where each combo is a list of abilities/items 
    '''

    herocombos = []

    i = 0
    while i < len(values)-1:
 
        j = i + 1
        combo = []

        combo.append(values[i][0])  # add first element
        start = values[i][1]        # timestamp
        next  = values[j][1]        # timestamp

        # cycle while the time is in the interval and we haven't reached the end of the list
        while (next-start <= interval) and (j<len(values)):
            combo.append(values[j][0])      # dismiss items/abilities called null
            j += 1
            try: 
                next = values[j][1]
            except:
                break     # in case the list ends
        
        # consider only lists with 2 or more elements
        if len(combo) > 1:
            herocombos.append(combo)

        i += j    # skip all elements already in a combo   

    return herocombos


def create_output(heroesdict, interval):
    '''
    This function creates a final structure with heronames, combos and number of occurrences of each combo
    INPUT:
        heroesdict: dictionary with all heroes and list of abilities/items
        interval: time interval to consider a succession is part of a combo
    OUTPUT:
        list structure with 3-tuples containing (heroname, combo, number of ocurrences of the combo)
    '''

    output = []
    for heroname, values in heroesdict.items():
        herocombos = create_combos(values, interval)

        for elem in herocombos:
            num = herocombos.count(elem)
            output.append((heroname, str(elem), num))

    return set(output)



def write_file(header, rows, filename):
    '''
    Write a CSV file with a header and the rows specified as a list
    INPUT:
        header: list of elements for the first row/header of the file
        rows: list of rows to write on the file
        filename: file to create/write
    OUTPUT:
        none
    '''

    with open(filename, 'w') as f:
        write = csv.writer(f)
        write.writerow(header)
        write.writerows(rows)


# Use timer to check performance
starttimer  = timeit.default_timer()
print("The start time is :", starttimer)

# load input file
df = load_file(FILENAME)   

# create a dictionary with all the Abilities and Items used by a Hero
heroesdict = create_dictionary(df.to_numpy(), ordered=True)

# calculate combos
combosdict = create_output(heroesdict, INTERVAL)

# create output file
header = ['Hero', 'Combo', 'Occurences']

write_file(header, combosdict, OUTPUT)

print('Ended in: ', timeit.default_timer() - starttimer)

