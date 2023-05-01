import difflib

def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    diff = difflib.unified_diff(lines1, lines2, lineterm='', fromfile=file1, tofile=file2)
    diff_str = '\n'.join(list(diff)[2:])  # Skip first two lines

    if diff_str:
        print('Differences found:')
        print(diff_str)
    else:
        print('No differences found.')

if __name__ == '__main__':
    file1 = input('Enter the path to the first file: ')
    file2 = input('Enter the path to the second file: ')
    compare_files(file1, file2)
