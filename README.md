# csvjinja
A python tool to generically apply the contents of a CVS file to a Jinja2 template.

The data from the CSV file is read in and applied to the template as a 2 dimensional array called `sheet`.

The sample tempates include an exmaple to generate a markdown table and to take contact information and build an html 
document for printing address labels .

## Usage
csvjinja.py [-h] [-d DELIMITER] [-q QUOTE] template_file [csv_file] [output_file]

### positional arguments:
<dl>
  <dt>template_file</dt>
  <dd>The file containing the Jinja2 template</dd>

  <dt>csv_file</dt>
  <dd>The input data file in csv format. Defaults to standard input</dd>
  
  <dt>output_file</dt>
  <dd>The output data file to write. Defaults to standard output</dd>
</dl>

### optional arguments:
<dl>
  <dt>-h, --help</dt>
  <dd>Show this help message and exit</dd>
 
  <dt>-d DELIMITER, --delimiter DELIMITER</dt>
  <dd>Set character used for field delimiter. Defaults to autodetect</dd>
  
  <dt>-q QUOTE, --quote QUOTE</dt>
  <dd>Set character used for quoting fields. Defaults to autodetect</dd>
</dl>

## Features
* CSV file available in template as `sheet`
* Command line arguments available in template as `args`

## Requirements
* Python
* python-jinja2

## Todo
* Store max column size for use in template formatting
* Support for arbitrary command line parameter passing into template
* Could a more functional approach to the design cut down the number of passes through the CSV file
