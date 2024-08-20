#!/bin/bash

print_help () {
    echo -e "\
Usage: ./utils.sh [-c] [--count_card] [-n] [--name-occurence] argument

COMMANDS:

-c directory, --count-card directory
    from a faction, take the faction directory as argument
    and count cards in list.txt

-n card_name, --name_occurence card_name
    find all occurences of a card_name, search in all faction's list.txt"
}

count_card () {
    DIR="$FACTION_DIR"/list.txt
    COUNT=$(sed "s/.*:.:\(.\)$/\1/g" "$DIR" | paste -sd+ - | bc)
    echo "Found $COUNT $FACTION_DIR cards."
}

name_occurence () {
    echo "TODO"
}

# PARSING

if [[ -z "$1" ]]; then print_help; exit 1; fi

POSITIONAL_ARGS=()
FACTION_DIR=
CARD_NAME=

while [[ $# -gt 0 ]]; do
  case "$1" in
    -c|--count-card)
      if [[ -z "$2" ]]; then print_help; exit 1; fi
      FACTION_DIR="$2"
      shift # past argument
      shift # past value
      ;;
    -n|--name-occurence)
      if [[ -z "$2" ]]; then print_help; exit 1; fi
      CARD_NAME="$2"
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

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

# RESOLUTION

if [[ $CARD_NAME ]]; then
    name_occurence
fi

if [[ $FACTION_DIR ]]; then
    count_card
fi

