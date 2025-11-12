#!/usr/bin/env python3
#    Upload gains from local file to api.
#    Tim Molteno 2023
#    Phill Brown 2023

import argparse
import csv
import neoden_kicad.converter as convert

if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(
        description="Convert KiCad files for use with Neoden YY1 pick and place machine.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--pos", type=str, required=True, help="POS file name.")
    parser.add_argument("--out", type=str, required=True, help="Output file name.")
    parser.add_argument("--feeder_map", type=str, required=False, help="Feeder map file name.")

    ARGS = parser.parse_args()

    # Read the CSV file here
    fname = ARGS.pos
    with open(fname, "r") as f:
        reader = csv.reader(f)
        data = list(reader)

    header = data.pop(0)
    new_data = []
    for row in data:
        new_data.append(dict(zip(header, row)))

    # Load the feeder map from the CSV file
    feeder_map = []
    if ARGS.feeder_map:
        with open(ARGS.feeder_map, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            feeder_map = list(reader)
        convert.update_feeder_map(feeder_map)
    else:
        print("\033[33mWarning:\033[0m No feeder map file specified. Feeder numbers will be set to '0'.")

    # Convert the input dictionary to the output dictionary
    output_neoden_csv_info = convert.neoden_csv_info(None)
    output_data, output_header = convert.convert(new_data)
    ## Write the new CSV file here
    with open(ARGS.out, "w") as f:
        writer = csv.writer(f)
        writer.writerows(output_neoden_csv_info)
        writer.writerow(output_header)
        writer.writerows(output_data)
