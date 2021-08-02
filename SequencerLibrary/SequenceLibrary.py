import os
import json
import csv
import pandas
from pandas.core.frame import DataFrame
import re

nucleotides: list = ['A', 'C', 'G', 'T']

# Import and Export Data
def csv2dataframe(file_path: str, head=False) -> DataFrame:
    with open(file_path, 'r') as csv_file:
        csv_dataframe = pandas.read_csv(csv_file, header=head)
    return csv_dataframe


def json2dict(file_path: str) -> dict:
    with open (file_path, 'r') as json_file:
        j = json.load(json_file)
    return j


def text2csv(file_path: str, deliniation=',', headers=[]):
    file_name, _ = os.path.splitext(file_path)
    _, file_name = os.path.split(file_name)
    out_file = file_name = '.csv'
    txt_dump = pandas.read_csv(file_path, delimiter=deliniation, names=headers)
    txt_dump.to_csv(out_file)


def write2csv(file_path: str, data_frame: DataFrame):
    with open(file_path, 'w+') as _:
        data_frame.to_csv(file_path)


def write2json(file_path: str, data: dict):
    with open(file_path, 'w+') as json_file:
        json.dump(data, json_file, indent=6)


# Adjust Data
def insert_column(dataframe: DataFrame, position: int, new_column_name: str, new_column_data: list):
    dataframe.insert(position, new_column_name, new_column_data)


def subset(dataframe: DataFrame, *args):
    headers = [name for name in args]
    sub_frame = dataframe[headers]

    return sub_frame


# def gene_search(dataframe: DataFrame, headers: (str or list), *genes, head=False, tail=False):
#     # genes = [name for name in genes]
#     if head:
#         dump_frame = dataframe[headers]
#         for gene in genes:
#             hdf = dump_frame[dump_frame.head]

# Transcriptions
def dna_transcription(dna: str) -> str:
    rna = re.sub('T', 'U', dna)
    transcription = rna[::-1]

    return transcription


def rna_transcription(rna:str) -> str:
    proteins: dict = json2dict('RNA_Protein.json')
    protein_chain: str = ''
    for codon, protein in proteins.items():
        if codon in rna:
            protein_chain = protein_chain + protein

    return protein_chain


# Sequencer
def sequencer(sequence: str, break_point: int, head=False, tail=False) -> tuple:
    h, t = '', ''
    for index, n in enumerate(sequence, 1):
        if index <= break_point:
            h = h + n
        elif index > break_point:
            t = t + n

    return h, t


def breakpoint_sequencer(sequence: str, break_point: int, upper_bound: int, lower_bound: int) -> str:
    b = ''
    for index, n in enumerate(sequence, 1):
        if (index >= break_point - lower_bound) and (index <= break_point + upper_bound):
            b = b + n

    return b


# Data Analysis
def nuc_search(sequence: str, target: str) -> list:
    nuc = re.findall(target, sequence)

    return nuc


def nuc_search_dataframe(dataframe: DataFrame, column_name: str, target: str) -> list:
    n = [len(nuc_search(sequence, target)) for sequence in dataframe[column_name]]

    return n


def slicer(sequence: str, index: str, head=False, tail=False, ends=False):
    if head:
        s = sequence[index: len(sequence): ]

        return s

    if tail:
        s = sequence[0: len(sequence) - index: ]

        return s

    if ends:
        s = sequence[index: len(sequence) - index: ]

        return s


def sequence_length(dataframe: DataFrame, column_name: str) -> list:
    l = [len(sequence) for sequence in dataframe[column_name]]

    return l


def nucleotide_positions(sequence: str, dictionary: dict):
    for p, n in enumerate(sequence, 1):
        for nuc in nucleotides:
            key = nuc + str(p)
            if re.match(nuc, n):
                dictionary[key].append(1)
            else:
                dictionary[key].append(0)