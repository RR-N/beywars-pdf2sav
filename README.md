## BEYWARS PDF2SAV

This program loads **.pdf**, extracts all of its interactive elements, and generates a **.sav** file according to specifications delineated in an accompanying config file. Features include (optional) type validation, flexible field selection, and... well, that's about it.

Written on request.

---

### <u>Installation</u>


In Git Bash:
1. `git clone https://github.com/RR-N/beywars-pdf2sav.git`
2. `cd beywars-pdf2sav`
3. `pip install -r requirements.txt`


### <u>Usage</u>


1. Configure config.ini according to examples.
	- The value of `validation-policy` determines what the program will do if an answer's data type does not match the one expected:
		 |Validation Policy|Description|   
		 |----|----|      
         |`continue`|Extract value and write to **.sav** regardless of type.|    
         |`skip`|Skip the entry in question but continue with the rest.|    
         |`cancel`|Skip the **.pdf** in question & print a list of skipped participants at the end.|    
         |`ask`|Ask on a case-by-case basis as the program encounters invalid entries.|
2. Place PDFs to be processed in the `input` folder.
3. Open a shell of your choice in the program folder.
4. Type `python main.py`.
	- Your **.sav** files will be in `output/spss`.
	- Successfully processed **.pdf** files are automatically moved from the input folder into `output/processed_pdfs`.