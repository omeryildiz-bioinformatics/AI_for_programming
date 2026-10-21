"""Calculate and print GC content for each record in a FASTA file."""

import argparse
import sys


def fasta_records(path):
    """Yield (header, sequence) pairs from a multi-record FASTA file."""
    header = None
    sequence = []

    with open(path) as fasta:
        for line_number, line in enumerate(fasta, start=1):
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(sequence)
                header = line[1:]
                sequence = []
            elif header is None:
                raise ValueError(
                    f"Sequence data before the first FASTA header at line {line_number}"
                )
            else:
                sequence.append(line)

    if header is not None:
        yield header, "".join(sequence)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate GC content for each record in a FASTA file."
    )
    parser.add_argument("fasta", help="path to a FASTA file")
    parser.add_argument(
        "--min-gc",
        type=float,
        help="only print records with GC content strictly above this percentage",
    )
    args = parser.parse_args()

    for header, sequence in fasta_records(args.fasta):
        if not sequence:
            print(f"Warning: skipping empty sequence for >{header}", file=sys.stderr)
            continue
        gc_percent = 100 * sum(base in "GgCc" for base in sequence) / len(sequence)
        if args.min_gc is not None and gc_percent <= args.min_gc:
            continue
        print(f">{header}\t{gc_percent:.3f}%")


if __name__ == "__main__":
    main()
