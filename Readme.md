# Project Goal
From an input Excel containing actions performed and items used by Dota players, we want to determine frequent combinations of actions commonly performed by certain heroes in a short period of time. We call these _Combos_ 

## Input Data
An Excel file in format xlsx containing a single sheet with three columns:
* Hero: The name of the hero
* Item: A list items used. Each element is a JSON object with two fields: "item" with the item name and "time" with a timestamp when was the item used
* Ability: A list of abilities invoked. Each element is a JSON object with two fields: "ability" with the name of the ability invoked and "time" with the timestamp when it was invoked

## Definitions

* __Combo:__ A rapid succession of items used and abilities invoked during a small predefined interval
__Interval:__ Time interval during which a sequence of abilities and items used can be considered a combo


## Outputs
The script generates a csv file containing three columns:
* Hero: The name of the hero/character
* Combo: The combo identified (succession of items and abilities)
* Occurrences: The number of times the hero executed the combo