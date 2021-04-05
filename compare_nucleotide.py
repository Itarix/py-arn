print("hello world")


def format_error(error_message, val1, val2, index):
    return f'Error: {error_message:30} => sequence 1 : {val1:1} vs sequence 2 : {val2:1} ==> at position {index:10d}'


def is_can_be_imbriquate(val1, val2):
    if val1 == "A" and val2 == "U":
        is_imbricate = True
    elif val1 == "C" and val2 == "G":
        is_imbricate = True
    else:
        is_imbricate = False
    return is_imbricate

error_percent = 30
sequence_1 = "UCGUACCGUGAGUAAUAAUGCGB"
sequence_2 = "UAACACUGUCUGGUAACGAUGU"

# jf true so it will add space before sequence 2
# If False so it will add space before sequence 1
add_space_sequence2 = False

size_sequence_1 = len(sequence_1)
size_sequence_2 = len(sequence_2)

min_size_sequence = size_sequence_2
max_size_sequence = size_sequence_1
if len(sequence_2) > len(sequence_1):
    min_size_sequence = size_sequence_1
    max_size_sequence = size_sequence_2

f = open("result.txt", "w")

nb_error = 0
for i in range(0, size_sequence_1):
    if size_sequence_1 != size_sequence_2 and (i == size_sequence_1 or i == size_sequence_2):
        print(
            format_error("Bad size sequences", sequence_1[i], " ", i)
        )
        f.write(format_error("Bad size sequences", sequence_1[i], " ", i) + "\n")
        nb_error = nb_error + 1
        break

    if sequence_1[i] != sequence_2[i]:
        print(
            format_error("Bad value", sequence_1[i], sequence_2[i], i)
        )
        f.write(format_error("Bad value", sequence_1[i], sequence_2[i], i) + "\n")
        nb_error = nb_error + 1

print("end")
f.write("end\n")
if nb_error > 0:
    print(f'Number of errors while analyse sequences =>  {nb_error:1d}')
    f.write(f'Number of errors while analyse sequences =>  {nb_error:1d}\n')

copy_sequence_2 = sequence_2
copy_sequence_1 = sequence_1
for i in range(0, size_sequence_1):
    if i > 0:
        if add_space_sequence2:
            copy_sequence_2 = " " + copy_sequence_2
        else:
            copy_sequence_1 = " " + copy_sequence_1

    size_sequence_1 = len(copy_sequence_1)
    size_sequence_2 = len(copy_sequence_2)

    nb_error_imbricate = 0
    print(f'Analyse => sequence 1 : {copy_sequence_1:1} vs sequence 2 : {copy_sequence_2:1}')
    f.write(f'Analyse => sequence 1 : {copy_sequence_1:1} vs sequence 2 : {copy_sequence_2:1}\n')
    for i in range(0, size_sequence_2):
        if size_sequence_1 != size_sequence_2 and (i + 1 == size_sequence_1 or i + 1 == size_sequence_2):
            print("end of sequences")
            f.write("end of sequences\n")
            break
        if is_can_be_imbriquate(copy_sequence_1[i], copy_sequence_2[i]):
            print(
                format_error("Can be imbricate", copy_sequence_1[i], copy_sequence_2[i], i)
            )
            f.write(format_error("Can be imbricate", copy_sequence_1[i], copy_sequence_2[i], i) + "\n")
            nb_error_imbricate = nb_error_imbricate + 1

    f.write(f'We have found : {nb_error_imbricate:1d} error. Percent {nb_error_imbricate/min_size_sequence*100:1.02f}\n')
    print(f'We have found : {nb_error_imbricate:1d} error. Percent {nb_error_imbricate/min_size_sequence*100:1.02f}')
    if nb_error_imbricate/min_size_sequence*100 > error_percent:
        print(f'Bad combination : {nb_error_imbricate/min_size_sequence*100:1.02f}%')
        f.write(f'Bad combination : {nb_error_imbricate/min_size_sequence*100:1.02f}%\n')

f.close()