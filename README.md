# sonar_tools
various tools for working with the sonar corpus repository

- sonar_to_raw: convert sonar500/DCOI files to raw text data (without the annotations) (expects data to be in dir '../sonarCorpus/SoNaRCorpus_NC_1.2/SONAR500/DCOI/' )
- concat: concatenate all files of the same topic into 1 big file, useful as datasources for prodigy (expects data to be in dir '../sonar_to_raw/output/')
