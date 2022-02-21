#!/bin/bash

helpFunction()
{
  echo ""
  echo "Usage: $0 --bondID ZXBL00000 --deviceName 'Test Device' --location 'Bedroom' --template RMS12 --quantity 10"
  echo -e "\t--bondID The ID of the Bond you want to create the new devices"
  echo -e "\t--deviceName The name of the device. This will be a prefix of the actual name. I.e: 'Test Device 1', 'Test Device 2'..."
  echo -e "\t--location The device location (Bedroom, Living Room, etc.)"
  echo -e "\t--template The device template name to be created (RCF84, A1, etc.)"
  echo -e "\t--quantity The amount of devices that will be created"
  exit 1 # Exit script after printing help
}

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      helpFunction
      exit 0
      ;;
    --bondID)
      bondID=$2
      shift # past argument
      shift # past value
      ;;
    --deviceName)
      deviceName=$2
      shift # past argument
      shift # past value
      ;;
    --template)
      template=$2
      shift # past argument
      shift # past value
      ;;
    --location)
      location=$2
      shift # past argument
      shift # past value
      ;;
    --quantity)
      quantity=$2
      shift # past argument
      shift # past value
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

# Print helpFunction in case parameters are empty
if [ -z "$bondID" ] || [ -z "$deviceName" ] || [ -z "$location" ] || [ -z "$template" ] || [ -z "$quantity" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
   exit 0
fi

echo "Looking for Bond $bondID..."
echo

bond discover
bond select $bondid

echo
echo "Adding $deviceName (1 to $quantity) with template $template to $bondID"

for (( i=1; i<=$quantity; i++ )); do
  name="$deviceName $(printf %0*d ${#quantity} $i)"
  bond devices create --name "$name" --location "$location" --template "$template"
done

echo "Done!"