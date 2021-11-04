
import pandas as pd
import argparse
from clinical_forms_util import clinical_forms_util
import os
import json
from io import StringIO


def get_nl_json_string(input_dict):
  return '\n'.join([str(i) for i in input_dict])

def main():
    parser = argparse.ArgumentParser(
        usage="%(prog)s --output-dataset <BQ dataset> --paying <project ID> --output-dir <dir> <excel_input>\n\n"
        "This tool will parse clinical data Excel spreadsheet following the template of ACRIN"
        )
    parser.add_argument(
        "--output-dataset", 
        "-b",
        dest="output_dataset",
        help="BigQuery dataset to store resulting dictionary tables",
        required=False
    )

    parser.add_argument(
        "--paying", 
        "-p",
        dest="paying",
        help="ID of the GCP project that will be used to charge for data egress (free if within the same region)",
        required=False
    )

    parser.add_argument(
        "--output-dir", 
        "-d",
        dest="output_dir",
        help="Directory that will be used to store the parsed content as JSON files",
        required=False
    )

    parser.add_argument(
        "--collection-id", 
        "-c",
        dest="collection_id",
        help="collection_id of the IDC collection this clinical data will accompany",
        required=True
    )

    parser.add_argument(
        dest="excel_file", 
        help="Input Excel file that follows organization of dictionary used in ACRIN TCIA collections"
    )

    args = parser.parse_args()

    parser = clinical_forms_util.DictionaryReader(args.excel_file)
    parser.parse_dictionaries()
    
    dict_names = parser.get_dictionary_names()
    if args.output_dir:
        for form_id in dict_names:
            with open(os.path.join(args.output_dir, f"{args.collection_id}_{form_id}_dict.json"), "w") as f:
                dict = parser.get_dictionary(form_id)
                f.write(get_nl_json_string(dict))
                print(f"Saved dictionary \"{form_id}\" with {len(dict)} items")
    print(f"Saved total of {len(dict_names)} dictionaries")
    with open(os.path.join(args.output_dir, f"{args.collection_id}_dict.json"), "w") as f:
        metadict = parser.get_meta_dictionary()
        f.write(get_nl_json_string(metadict))
        print(f"Saved metadictionary with {len(metadict)} items")
if __name__ == "__main__":
    main()