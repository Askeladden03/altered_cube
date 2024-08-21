#!/bin/bash

positional_args=()
faction_dir=
card_name=
factions=("axiom" "bravos" "lyra" "muna" "ordis" "yzmir")

print_help () {
    echo -e "\
Usage: ./utils.sh [-c] [--count_card] [-n] [--name-occurence] argument

COMMANDS:

-c directory, --count-card directory
    Count cards for a faction.
    directory can be [axiom|bravos|lyra|muna|ordis|yzmir|all]

-n card_name, --name_occurence card_name
    Find all occurences of a card_name, search in all faction's list.txt"
}

count_card () {
    dir="$faction_dir"/list.txt
    count=$(sed "s/.*:.:\(.\)$/\1/g" "$dir" | paste -sd+ - | bc)
    echo "Found $count $faction_dir cards."
}

name_occurence () {
    n=0
    while [[ n -lt ${#factions[@]} ]]
    do
        search_in_faction ${factions[$n]}
        n=$((n + 1))
    done
}

search_in_faction () {
    faction="$1"
    grep "$card_name" "$faction"/list.txt |\
    sed "s/^\(.*\):\(.\):\(.\)$/$faction: \3 \1 \2/g"
}

# PARSING

if [[ -z "$1" ]]; then print_help; exit 1; fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    -c|--count-card)
      if [[ -z "$2" ]]; then print_help; exit 1; fi
      faction_dir="$2"
      shift # past argument
      shift # past value
      ;;
    -n|--name-occurence)
      if [[ -z "$2" ]]; then print_help; exit 1; fi
      card_name="$2"
      shift # past argument
      shift # past value
      ;;
    *)
      echo "Unknown option $1"
      print_help
      exit 1
      ;;
  esac
done

set -- "${positional_args[@]}" # restore positional parameters

# RESOLUTION

if [[ $card_name ]]; then
    name_occurence
fi

if [[ $faction_dir ]]; then
    if [[ $faction_dir == "all" ]] then
        n=0
        while [[ n -lt ${#factions[@]} ]]
        do
            faction_dir=${factions[$n]}
            count_card
            n=$((n + 1))
        done
    else
        count_card
    fi
fi

