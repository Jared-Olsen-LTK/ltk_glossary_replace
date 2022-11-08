# ltk_glossary_replace

Note this requires "json", "requests", and "time" python libraries, and uses python 3.

1. Create a new glossary while assumed as your TMS community's admin user.
2. Upload your glossary file into the new glossary.
3. When the import process finishes, run this script.
      * It's good to check if the glossary got at least some of the entries before running.
      * Also check if the new glossary is listed on at least project (instead of the old one) before you do step 4.
      * Script tells you all the projects that it runs on, and how many requests it had to make to run in its entirety.
4. Delete the old glossary.

The script will print() you all the projects it will try to run on, and if a project has the old master, it will replace it with the new. 
If the old master is not present, it will not replace it.
