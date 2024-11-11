import os
from time import time
from multiprocessing import Pool
from scanner import *

# Process the downstream sequence
def getDis(row):
    dist = np.abs(row['Minus10_3end_coordinate'] - row['TSS_coordinate'])
    if dist == 1: return '*'
    return row['DOWN'][:(dist-2)]

def getStart(row):
    dist = np.abs(row['Minus10_3end_coordinate'] - row['TSS_coordinate'])
    if dist == 1: return row['Minus10'][-1] + row['DOWN'][:2]
    return row['DOWN'][(dist-2):(dist+1)]

def getITR(row):
    dist = np.abs(row['Minus10_3end_coordinate'] - row['TSS_coordinate'])
    return row['DOWN'][(dist+1):(dist+101)]

# Function to process each TSS group in parallel
def process_tss_group(args):
    species, df_tss = args

    g = df_tss["Genome_accession"].iloc[0]
    file_g = current_directory + "/../genomes/" + g + ".gb"
    genome = Genome(next(SeqIO.parse(open(file_g, "r"), "genbank")))
    genome_copied = deepcopy(genome)  # for tss_shuffle

    print(species)

    tss = []
    tss_random = []
    tss_shuffle = []

    for _, row in df_tss.iterrows():
        direction = row["Direction"]
        tss_loc = int(row["TSS_coordinate"])

        direction_random = random.choice(['+', '-'])
        tss_loc_random = random.choice(range(100, genome.length-100)) + 1

        tss.append(scan_promoter(tss_loc, direction, genome, tss_m10_range))
        tss_random.append(scan_promoter(tss_loc_random, direction_random, genome, tss_m10_range))
        tss_shuffle.append(scan_promoter_shuffle(tss_loc, direction, genome_copied, tss_m10_range))

    ## TSS
    df_tss["Minus10_3end_coordinate"] = [t[0].getLoc_m10_end() for t in tss]
    df_tss["UP"] = [str(get_element_UP(t[0])) for t in tss]
    df_tss["Minus35"] = [str(t[0].getSequence()[:6]) for t in tss]
    df_tss["Spacer"] = [str(t[0].getSequence()[6:-6]) for t in tss]
    df_tss["Minus10"] = [str(t[0].getSequence()[-6:]) for t in tss]
    df_tss["DOWN"] = [str(get_element_DOWN(t[0])) for t in tss]
    
    df_tss["Dis"] = df_tss.apply(getDis, axis="columns")
    df_tss["Start"] = df_tss.apply(getStart, axis="columns")
    df_tss["ITR"] = df_tss.apply(getITR, axis="columns")
    
    df_tss.drop(columns=["Species", "Genome_accession", "DOWN"], inplace=True)
    df_tss.to_csv(current_directory + f"/../tables/{species}.tsv", sep='\t', index=False)

    ## TSS random
    df_tss_random = pd.DataFrame({
        "TSS_coordinate": [t[1][0] for t in tss_random],
        "Direction": [t[1][1] for t in tss_random],
        "Minus10_3end_coordinate": [t[0].getLoc_m10_end() for t in tss], 
        "UP": [str(get_element_UP(t[0])) for t in tss_random],
        "Minus35": [str(t[0].getSequence()[:6]) for t in tss_random],
        "Spacer": [str(t[0].getSequence()[6:-6]) for t in tss_random],
        "Minus10": [str(t[0].getSequence()[-6:]) for t in tss_random],
        "DOWN": [str(get_element_DOWN(t[0])) for t in tss_random],
        })
    
    df_tss_random["Dis"] = df_tss_random.apply(getDis, axis="columns")
    df_tss_random["Start"] = df_tss_random.apply(getStart, axis="columns")
    df_tss_random["ITR"] = df_tss_random.apply(getITR, axis="columns")
    
    df_tss_random.drop(columns=["DOWN"], inplace=True)
    df_tss_random.to_csv(current_directory + f"/../tables/{species}_random.tsv", sep='\t', index=False)

    ## TSS shuffle
    df_tss_shuffle = deepcopy(df_tss)
    df_tss_shuffle["Minus10_3end_coordinate"] = [t[0].getLoc_m10_end() for t in tss_shuffle]
    df_tss_shuffle["UP"] = [str(get_element_UP(t[0])) for t in tss_shuffle]
    df_tss_shuffle["Minus35"] = [str(t[0].getSequence()[:6]) for t in tss_shuffle]
    df_tss_shuffle["Spacer"] = [str(t[0].getSequence()[6:-6]) for t in tss_shuffle]
    df_tss_shuffle["Minus10"] = [str(t[0].getSequence()[-6:]) for t in tss_shuffle]
    df_tss_shuffle["DOWN"] = [str(get_element_DOWN(t[0])) for t in tss_shuffle]
    
    df_tss_shuffle["Dis"] = df_tss_shuffle.apply(getDis, axis="columns")
    df_tss_shuffle["Start"] = df_tss_shuffle.apply(getStart, axis="columns")
    df_tss_shuffle["ITR"] = df_tss_shuffle.apply(getITR, axis="columns")
    
    df_tss_shuffle.drop(columns=["DOWN"], inplace=True)
    df_tss_shuffle.to_csv(current_directory + f"/../tables/{species}_shuffle.tsv", sep='\t', index=False)


if __name__ == '__main__':

    t_start = time()

    ## The range of the Minus10-TSS distance
    # tss_m10_range = [-10, 20]
    # tss_m10_range = [1, 11]
    tss_m10_range = [0, 14]
    # print(tss_m10_range)
    
    # global date
    # date = '20240411'
    # print(date)

    global current_directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    TSS = pd.read_csv(current_directory + "/../TSS_List.tsv", sep="\t")

    ## Split TSS dataframe into chunks for parallel processing
    chunks = [(i, group) for i, group in TSS.groupby("Species")]

    ## Create a Pool of processes and map the processing function to the chunks
    with Pool(4) as pool:
        pool.map(process_tss_group, chunks)

    t_end = time()
    print(f"time usage: {int(t_end-t_start)} seconds")
