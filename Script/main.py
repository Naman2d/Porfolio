from test import *

parse_fastq("/Users/nitin/BioInfo-Project/Portfolio/port/Porfolio/data/control_psbA3.fastq")

def main():         #defining a list for ACGT counts
    list=["A","C","G","T"]

    records = parse_fastq(filename="/Users/nitin/BioInfo-Project/Portfolio/port/Porfolio/data/control_psbA3.fastq")   #calling 
    compute_stats(records)
    compute_gc_content(records)
    cleanup_csv()
    for a in range(0,len(list)):
        count_acgt(records, list[a])
    plot_acgt_bar()


main()


# total_bases2 =""
# for rec in records:
#     return sum(len[rec])
# count_acgt()