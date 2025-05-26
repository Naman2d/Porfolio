#defining a function for parsing a fastq file to access quality score.
import os
import time
import matplotlib.pyplot as plt
import csv

csv_output= "/Users/nitin/BioInfo-Project/Portfolio/Fastq_c/people.csv"
ACGT_list=[]
counts=[]

def parse_fastq(filename): #FASTQ is file format used in bioinformatics (stores both nucleotide and and quality score)
    records = []

    with open (filename, 'r') as fq:
        while True:
            header = fq.readline().strip()
            if not header:
                break

            sequence = fq.readline().strip()
            plus = fq.readline().strip()
            quality = fq.readline().strip()
            record = {
                'id': header[1:], #(ID for sequence)
                'seq': sequence,  #(DNA sequence "string of ACGT")
                'qual': quality   # (quality score- "indicates the probability of an incorrect base call")
            }
            records.append(record)
        return records
    
def compute_stats(records):
    total_reads = len(records)          #(MOre reads are better , helps determine sequencing depth)
    total_bases = sum(len(r['seq']) for r in records)       #(Shows how much raw sequencing data was generated)
    avg_read_length = total_bases / total_reads             #(Determine if reads are long enough for alignment or assembly)

    def qual_score(qscr):                           #(Confidence level in each base call, better score = accuracy and reliability)
        return[ord(char) - 33 for char in qscr]
    
    total_quality = sum(sum(qual_score(rec['qual']))for rec in records)  
    total_qual_bases = sum(len(rec['qual']) for rec in records)
    avg_quality = total_quality/total_qual_bases

    print(f"Total reads: {total_reads}")
    print(f"Average Read length: {avg_read_length:.2f}")
    print(f"AVerage base quality score: {avg_quality:.2f}")         #(if low quality may need to be trimmed/ filtered)

def compute_gc_content(records):                        #(Higher GC = More stable )
    def gc_percentage(seq):
        gc_count = seq.count('G') + seq.count('C')
        return (gc_count/len(seq)) * 100 
    
    gc_contents = [gc_percentage(rec['seq']) for rec in records]
    avg_gc = sum(gc_contents) / len(gc_contents)

    print(f"Average GC content : {avg_gc:.2f}")

def count_acgt(records,string_point):           # (Unusual distribution may indicate sequencing error)
    type_data = 0

    for record in records:
        sequence = record ['seq']    #extracting and storing sequence from dictionary
        type_data += sequence.count(string_point)
    print(f"Count {string_point} : {type_data}")
    output_data(string_point,type_data)

def plot_acgt_bar():                    #creating a plot for ACGT counts filter  any baises in the data)
    opening_csv(csv_output)
    plt.figure(figsize = (6,4))
    plt.bar(ACGT_list, counts, color=['blue', 'green', 'orange', 'red'])
   
    plt.title("BAse counts in FASTQ Sequences")
    plt.xlabel("Base")
    plt.ylabel("Count")
    plt.ylim(0, max(counts) + 5000)

    plt.grid(axis="y", linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

def cleanup_csv():                      #outputting ACGT data in a separate file
    if os.path.exists(csv_output):
        os.remove(csv_output)
    print("Cleanup done")

def output_data(a,b):    
    data = [
        [a, b]
    ]

    file_exists = os.path.isfile(csv_output)
    with open(csv_output, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print("Data appended successfully to", csv_output)


    # Read data back from the same CSV file
def opening_csv(csv_output):
    
    with open(csv_output, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            ACGT_list.append(row[0])
            counts.append(int(row[1]))
            
        

    

# plot_acgt_bar(records)


#print(type(acgt))



# if __name__ == '__main__':
#     fastq_file = 