def split_recursive(text, separators, chunk_size):
    sep = separators[0]                                  # biggest boundary to try first
    pieces = text.split(sep)                             # cut the text on it
    chunks = []
    for piece in pieces:
        if len(piece) <= chunk_size:                     # small enough → keep as-is
            chunks.append(piece)
        elif len(separators) > 1:                        # too big → retry with finer separator
            chunks += split_recursive(piece, separators[1:], chunk_size)
        else:                                            # no separators left → forced to keep
            chunks.append(piece)
    return chunks

text = "We are open Tuesday to Sunday.\nWe close on Mondays.\n\nStarters cost 6 euros. Mains cost 15 euros. Desserts cost 5 euros."
seps = ["\n\n", "\n", ". "]
for i, c in enumerate(split_recursive(text, seps, 40)):
    print(i, repr(c))