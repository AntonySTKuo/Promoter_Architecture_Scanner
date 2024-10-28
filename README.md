# TSS Scanner

**Transcriptional Start Site (TSS) Scanner** is a tool designed to segment and align promoter elements upstream of TSS in bacteria by combining TSS-mapping data.

In [this article](url), we used various bacterial genomes listed in **Genome_List.csv**. Their GenBank files are zipped in the **Genomes** folder; please unzip them before use. The TSS-mapping data we collected is provided in the table **TSS_List.tsv**.

To reproduce the results of the article, run the Python script:

```bash
python scripts/scanner_multiprocessing.py
```

If you want to use your own data, replace the TSS table **TSS_List.tsv** with your data and place the corresponding genome GenBank files in the **Genomes** folder.

## Environment

The required environment is specified in **environment.yml**.

## Citation

[Article Title](url)

## License

&copy; 2024 David Chou Lab, Life Science Department, National Taiwan University

## Contact Information

For any inquiries, please contact:

**Antony Kuo**  
Email: [antonykuo@ntu.edu.tw](mailto:antonykuo@ntu.edu.tw)