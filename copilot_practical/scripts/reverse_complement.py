# reverse_complement.py
# Reads a single-record DNA FASTA file and prints its reverse complement.

COMPLEMENT = {"A": "T", "T": "A", "C": "G", "G": "C"}

def read_fasta_sequence(path):
    """Return the sequence from a single-record FASTA file."""
    sequence = []
    has_header = False

    with open(path) as fasta:
        for line in fasta:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if has_header:
                    raise ValueError("Expected a single-record FASTA file")
                has_header = True
            else:
                if not has_header:
                    raise ValueError("Expected a FASTA header before the sequence")
                sequence.append(line)

    if not has_header:
        raise ValueError("FASTA file has no header")
    if not sequence:
        raise ValueError("FASTA file has no sequence")
    return "".join(sequence)

def reverse_complement(seq):
    """Return the reverse complement of a DNA sequence."""
    try:
        return "".join(COMPLEMENT[base] for base in reversed(seq))
    except KeyError as error:
        raise ValueError("Sequence must contain only characters in 'ATCG'") from error

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Print the reverse complement of a FASTA sequence.")
    parser.add_argument("fasta", help="single-record FASTA input file")
    args = parser.parse_args()

    seq = read_fasta_sequence(args.fasta)
    print(reverse_complement(seq))