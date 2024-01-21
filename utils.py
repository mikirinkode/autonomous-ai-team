import os

def create_html_file(file_name, html_content):
    folder_path = 'output'
    file_path = f'{folder_path}/{file_name}.html'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(file_path, 'w') as file:
        file.write(html_content)