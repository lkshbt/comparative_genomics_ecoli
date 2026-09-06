from Bio.Seq import Seq

sequence = Seq("AGTACACTGGT")

print("Original sequence:", sequence)
print("\nSequence length:", len(sequence))
print("\nRNA sequence:", sequence.transcribe())
print("\nprotein sequence:", sequence.translate())
print("\nReverse complement:", sequence.reverse_complement())
