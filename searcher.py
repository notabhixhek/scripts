from rich.progress import Progress
import os
import time

def find_keyword_and_write_lines(input_file, keyword, output_file):
    with open(input_file, 'r', encoding='latin-1') as file:
        lines = file.readlines()

    found_count = 0

    with Progress() as progress:
        task = progress.add_task("[cyan]Processing...", total=len(lines))
        for i, line in enumerate(lines):
            progress.update(task, advance=1)

            if keyword in line:
                found_count += 1
                start_line = max(0, i - 1)
                end_line = min(i + 3, len(lines))
                selected_lines = lines[start_line:end_line]
                with open(output_file, 'a', encoding='utf-8', errors='replace') as output:
                    output.write(f"Instance {found_count} in {os.path.basename(input_file)}:\n")
                    output.writelines(selected_lines)
                    output.write("\n")

    if found_count == 0:
        print(f"No instances of the keyword found in {os.path.basename(input_file)}.")
    else:
        print(f"{found_count} instance(s) found in {os.path.basename(input_file)}.")

    return found_count

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    user_keyword = input("Enter the keyword to search: ")

    output_file = f"{user_keyword}_output.txt"

    # Get a list of all files in the directory
    files_in_directory = os.listdir(directory)

    # Filter only the text files
    text_files = [file for file in files_in_directory if file.endswith(".txt")]

    if not text_files:
        print("No text files found in the directory.")
    else:
        total_found_count = 0
        start_time = time.time()  # Record start time
        for text_file in text_files:
            input_file = os.path.join(directory, text_file)
            print(f"Processing file: {text_file}")
            file_found_count = find_keyword_and_write_lines(input_file, user_keyword, output_file)
            total_found_count += file_found_count

        end_time = time.time()  # Record end time
        time_taken = end_time - start_time

        if total_found_count == 0:
            print(f"No instances of the keyword found in any file.")
            try:
                os.remove(output_file)
            except FileNotFoundError:
                pass
        else:
            print(f"Total instances found in all files: {total_found_count}")
            print(f"Time taken: {time_taken:.2f} seconds")
            print(f"Output written to {output_file}")

    print("Processing completed.")