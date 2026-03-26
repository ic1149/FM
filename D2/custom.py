def printmat(mat, pad=" ", newline=True, min_len=1):
    pad_num = min_len + 0
    if iter(mat):
        try:
            iter(mat[0])
        except TypeError:
            for item in mat:
                if len(str(item)) > pad_num:
                    pad_num = len(str(item))

            out_items = ""
            for item in mat:
                out_items += str(item)\
                      + pad*(pad_num-len(str(item))) + ", "

            print(f"[{out_items[:-2]}]")
        else:
            for item in mat:
                printmat(item, pad=pad, newline=False, min_len=pad_num)

    else:
        print(mat)

    if newline:
        print()
