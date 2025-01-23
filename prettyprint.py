

def print_with_border(art, border_char="#", padding=2):
    # Split input text into lines
    lines = art.splitlines()

    # Find the maximum line length
    max_length = max(len(line) for line in lines)

    # Compute total width including padding and borders
    total_width = max_length + padding * 2

    # Print top border
    print(border_char * (total_width + 2))

    # Print each line centered within the border
    for line in lines:
        centered_line = line.center(max_length)
        print(f"{border_char}{' ' * padding}{centered_line}{' ' * padding}{border_char}")

    # Print bottom border
    print(border_char * (total_width + 2))