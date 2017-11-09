
def replace_in_file(file, new_file, replace_tuples):
    """
    Replaces words in the given file and stores the result in the new_file
    :param file: file to replace the values in
    :param new_file: place to store the result
    :param replace_tuples: (old_value, new_value)[]
    :return:
    """

    with open(file, "r") as f:
        with open(new_file, "w") as nf:
            for l in f.readlines():
                for (old_value, new_value) in replace_tuples:
                    l =l.replace(old_value, new_value)
                nf.write(l)
