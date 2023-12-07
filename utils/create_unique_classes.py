def create_numbers_file(file_path, start, end):
    with open(file_path, 'w') as file:
        for number in range(start, end + 1):
            file.write(f'{number}\n')

def main():
    output_file = 'unique_classes_num.txt'
    start = 0
    end = 757
    create_numbers_file(output_file, start, end)

if __name__ == "__main__":
    main()
