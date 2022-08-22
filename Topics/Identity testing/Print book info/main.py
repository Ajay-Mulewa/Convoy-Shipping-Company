def print_book_info(title, author=None, year=None):
    if author and year:
        print(f'"{title}" was written by {author} in {year}')
    elif author:
        print(f'"{title}" was written by {author}')
    elif year:
        print(f'"{title}" was written in {year}')
    else:
        print(f'"{title}"')
