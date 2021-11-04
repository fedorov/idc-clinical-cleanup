'''
WARNING: for the sake of expediency, this script is expected to run from Google Colab
'''

try:
    from google.colab import auth 
    from google.cloud import bigquery

    import argparse
    import os
    import json

    def load_dict_into_bq(project, dataset, nl_json_filename):

        # Construct a BigQuery client object.
        client = bigquery.Client(project=project)

        table = nl_json_filename.split("/")[-1].split(".")[-2]

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON, autodetect=True,
        )

        table_id = f"{project}.{dataset}.{table}"

        with open(file_path, "rb") as source_file:
            job = client.load_table_from_file(source_file, table_id, job_config=job_config)

        try:
            job.result()  # Waits for the job to complete.

            table = client.get_table(table_id)  # Make an API request.
            print(
                "Loaded {} rows and {} columns to {}".format(
                    table.num_rows, len(table.schema), table_id
                )
            )
        except:
            print(f"Failed to import {form_id} into BQ")
        

    def main():
        parser = argparse.ArgumentParser(
            usage="%(prog)s --output-dataset <BQ dataset> --paying <project ID> --input-dir <dir>\n\n"
            "This tool will import newline delimited JSONs from a folder into a BQ dataset"
            )
        parser.add_argument(
            "--output-dataset", 
            "-b",
            dest="output_dataset",
            help="BigQuery dataset to store resulting dictionary tables",
            required=True
        )

        parser.add_argument(
            "--paying", 
            "-p",
            dest="paying",
            help="ID of the GCP project that will be used to charge for data egress (free if within the same region)",
            required=True
        )

        parser.add_argument(
            "--input-dir", 
            "-d",
            dest="input_dir",
            help="Directory that contains New Line delimited JSON content to be imported into BQ",
            required=True
        )

        args = parser.parse_args()

        for filename in os.listdir(args.input_dir):
            load_dict_into_bq(args.project, args.output_dataset, filename)

    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print("WARNING: for the sake of expediency, this script can only be used from Google Colab!")