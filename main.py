import os
from art import text2art #shut up
import configparser
import pandas as pd
import pyreadstat
from PyPDF2 import PdfFileReader

response_dir = 'input'
spss_dir = 'output/spss'
proc_dir = 'output/processed_pdfs'
skipped_files = []
file_count = 0

def pdfProcessor(filename, file):
    reader = PdfFileReader(open(file, 'rb'))
    input_dict = reader.getFields()
    df = pd.DataFrame(index=config.keys(), columns=input_dict.keys())

    for idx, each_field in enumerate(input_dict):

        if each_field in config.keys() and type(input_dict[each_field]['/V']) == types[idx]:
            df[each_field] = input_dict[each_field]

        elif each_field in config.keys() and type(input_dict[each_field]['/V']) != types[idx]:

            if config['DEFAULT']['validation_policy'].lower() == 'ask':
                print(f"... WARNING! {each_field} answer's expected type is {types[idx]}, but it is actually {type(input_dict[each_field]['/V'])}.")
                option = input("\n... Type 'y' to accept it anyway, 'n' to skip it, or 'c' to skip participant: ")

                if option.lower() == 'y':
                    df[each_field] = input_dict[each_field]

                elif option.lower() == 'n':
                    print(f"... Skipping {each_field} entry at user's request.")

                elif option.lower() == 'c':
                    print(f"... Skipping {filename}.pdf at user's request.")
                    skipped_files += [filename]

            elif config['DEFAULT']['validation_policy'].lower() == 'continue':
                df[each_field] = input_dict[each_field]['/V']

            elif config['DEFAULT']['validation_policy'].lower() == 'skip':
                print(f"... Skipping {each_field} entry due to invalid type.")

            elif config['DEFAULT']['validation_policy'].lower() == 'cancel':
                print(f"... Skipping {filename}.pdf due invalid type.")
                skipped_files += [filename]

            else:
                print(f"... Invalid input. Skipping {filename} file.")

        else:
            print(f"... Skipping {each_field} entry because it is not listed in config.ini!")

    pyreadstat.write_sav(df, f"{spss_dir}/{filename}.sav", file_label=filename, column_labels=labels)

config = configparser.ConfigParser()
config.read('config.ini')
labels = [config[each_section]['label'] for each_section in config.sections()]
types = [config[each_section]['type'] for each_section in config.sections()]

print(text2art("\n\nBeywars",font='alligator2'))
print(text2art("PDF2SAV",font='alligator2'))
print("\nSettings extracted from config.ini:")

if config['DEFAULT']['validation_policy'].lower() == 'ask':
    print(f"Validation policy set to {config['DEFAULT']['validation_policy']}, user will be prompted on invalid entry.")
elif config['DEFAULT']['validation_policy'].lower() == 'continue':
    print(f"Validation policy set to {config['DEFAULT']['validation_policy']}, types will not be validated.")
elif config['DEFAULT']['validation_policy'].lower() == 'skip':
    print(f"Validation policy set to {config['DEFAULT']['validation_policy']}, invalid entries will be skipped.")
elif config['DEFAULT']['validation_policy'].lower() == 'cancel':
    print(f"Validation policy set to {config['DEFAULT']['validation_policy']}, skipping files with invalid entries.")
else:
    print(f"ERROR!\n"
          f"Validation policy set incorrectly (should be either ask, continue, skip, or cancel).\n"
          f"Quitting program.")
    quit()

print("\nExtracting following fields:\n- ", end ="")
print(*config.sections(), sep='\n- ')
print("\nProcessing response files...")

for each_file in os.listdir(response_dir):
    f = os.path.join(response_dir, each_file)
    if not f.endswith(".pdf"):
        continue
    else:
        file_count += 1
        pdfProcessor(each_file, f)
        os.replace(f, f"{proc_dir}/{each_file}")
        print(f"... Processed {each_file}.pdf.\n")

print(f"Successfully processed {file_count-len(skipped_files)} files, skipped {skipped_files}.")