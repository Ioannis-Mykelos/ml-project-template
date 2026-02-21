import argparse
import datetime as dt

from preprocessing import preprocessing_pipeline
from scoring import scoring_pipeline

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    """If the data for your project is avaiable in the datalake please input it in the project_config.
    For the each FileDataset type you have you will need to add an argument with the same name as
    the name of the dataset. So if the name of the dataset is input_data, the argument below would work."""
    # parser.add_argument("--input_data", type=str, help="input datapath argument")
    parser.add_argument("--output_data", type=str, help="output datapath argument")
    parser.add_argument(
        "--outfile_format_string",
        type=str,
        help="format of file containing predictions",
    )
    args = parser.parse_args()
    # The arguments can now be used as args.output_data etc
    date = dt.datetime.now().strftime("%Y-%m-%d")
    output_file_name = args.outfile_format_string.format(date=date)

    """ Please use the output_file_name as the name for your output. It's composed out of the
    project name (from project_config.json) + the date the pipeline is run """
