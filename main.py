#!/usr/bin/env python
""" Provides the base plumbing needed to pipe csv into jinga2 templates. """

# Imports
import sys
import csv
import jinja2
import argparse
import copy
import StringIO

# Constants and Data Tables

# Functions
def parse_args():
    """ Returns the processed results of the commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("template_file", help="The file containing the Jinja2 "
                        "template")
    parser.add_argument("csv_file", nargs="?", default="-", help="The input "
                        "data file in csv format. Defaults to standard input")
    parser.add_argument("output_file", nargs="?", default="-", help="The output"
                        " data file to write. Defaults to standard output")
    parser.add_argument("-d", "--delimiter", default="", help="Set character "
                        "used for field delimiter. Defaults to autodetect")
    parser.add_argument("-q", "--quote", default="", help="Sxet character used"
                        " for quoting fields. Defaults to autodetect")
    return parser.parse_args()

def get_sheet(file_in, args):
    """ Returns the data from the csv file in a two dimensional list, using the
    args to override guesses as to how to intterpret the data"""
    try:
        dialect = csv.Sniffer().sniff(file_in.read(16384), "\t;,")
    except csv.Error:
        # that didn't work, just assume it is excel format
        dialect = copy.copy(csv.excel)

    # Command line delimiter overrides
    if args.delimiter != "":
        dialect.delimiter = args.delimiter

    if args.quote != "":
        dialect.quotechar = args.quote

    file_in.seek(0)
    return list(csv.reader(file_in, dialect=dialect))

def get_template(filename):
    """ Returns a template parser based on the template in the supplied
    filename """
    # The search path can be used to make finding templates by
    #   relative paths much easier.  In this case, we are using
    #   absolute paths and thus set it to the filesystem root.
    template_loader = jinja2.FileSystemLoader(searchpath="./")

    # An environment provides the data necessary to read and
    #   parse our templates.  We pass in the loader object here.
    template_env = jinja2.Environment(loader=template_loader)

    # Read the template file using the environment object.
    # This also constructs our Template object.
    return template_env.get_template(filename)

# Main
def main():
    """ The main function execution starts here """
    # Get arguments
    args = parse_args()

    # load jinja2 template
    template = get_template(args.template_file)

    # load csvfile into sheet
    if args.csv_file == "-":
        input_wrapper = StringIO.StringIO(sys.stdin.read())
        sheet = get_sheet(input_wrapper, args)
        input_wrapper.close()
    else:
        with open(args.csv_file, 'rb') as file_in:
            sheet = get_sheet(file_in, args)

    # run jinja2 template with sheet
    template_vars = {"args"  : args,
                     "sheet" : sheet}

    # save output
    if args.output_file == "-":
        print template.render(template_vars)
    else:
        with open(args.output_file, 'wb') as file_out:
            file_out.write(template.render(template_vars))

# Standard Main call to avoid global namespace
if __name__ == "__main__":
    main()
