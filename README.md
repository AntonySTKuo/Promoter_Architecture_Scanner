# Promoter Architecture Scanner

**Promoter Architecture Scanner** is a tool designed to segment and align promoter elements upstream of TSS in bacteria. Detailed algorithms and methodologies are provided in the accompanying article.

In this article, we used various bacterial genomes listed in [**Genome_List.csv**](Genome_List.csv). Their GenBank files are located in the [**genomes**](genomes/) folder. The TSS-mapping data we collected is provided in the [**TSS_List.tsv**](TSS_List.tsv) table. The segmentation results are in the [**tables**](tables/) folder.

To reproduce the results presented in the article, run the following Python script:

```bash
python scripts/scanner_multiprocessing.py
```

If you wish to use your own data, replace the [**TSS_List.tsv**](TSS_List.tsv) file with your data and place the corresponding genome GenBank files in the [**genomes**](genomes/) folder.

## Environment

The required environment is specified in [**environment.yml**](environment.yml). To set up the environment using **conda**, run:

```bash
conda env create -f environment.yml
```

## Citation

[Unraveling the start element and regulatory divergence of core promoters across the domain Bacteria](https://www.biorxiv.org/content/10.1101/2025.01.23.634641v2)

## License

© 2024 David Chou Lab, Department of Life Science, National Taiwan University

## Contact Information

For any inquiries, please contact:

**Antony Kuo**  
Email: [antonykuo@ntu.edu.tw](mailto:antonykuo@ntu.edu.tw)

**David Chou**  
Email: [chouhh@ntu.edu.tw](mailto:chouhh@ntu.edu.tw)
