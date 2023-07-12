# Produce Issue Galleys for Seismica

This script produces issue galleys for Seismica. It uses input from the OJS API and the XML files produced by the SCE team to output:
- An imprint of the issue with all volunteers involved and their ORCID ids
- A table of contents
- A cover galley with the issue cover, the imprint and the TOC
- An issue galley with the cover galley and the PDFs galleys of all the articles, destined to be printed.
All of the data is downloaded from OJS API or website, you only need the login and password of a Seismica journal manager.

## Requirements
1. Create a conda environment if needed
    ```
    conda create -n ojs -c conda-forge python=3.7 numpy zlib sqlite pillow pandas openssl lxml beautifulsoup4 urllib pypdf 
    ```
2. Clone the edstats github repo to your local machine.  `cd` into the desired directory and clone using - 
    ```
    git clone https://github.com/WeAreSeismica/edstats.git
    ```
3. Install edstats
    ```
    python setup.py install
    ```
4. Clone the issue-galleys github repo to your local machine.  `cd` into the desired directory and clone using - 
    ```
    git clone https://github.com/WeAreSeismica/issue-galleys.git
    ```
5. Create a file `ojssecret.py` with the login & password of a `Journal Manager` user

6. Run issue.py with
    ```
    python issue.py -v 1 -n 1 -o /path/to/output/dir/
    ```
    Arguments are: 
    - -v: issue volume (int)
    - -n: issue number (int)
    - -o: output directory (str)
    - --tex or --no-tex: run LuaTeX (--tex). Default is True, --no-tex is for running LuaTeX via a separate editor (use if you want to manually edit the .tex)
    
