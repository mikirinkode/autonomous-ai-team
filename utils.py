import os

def create_html_file(file_name, html_content):
    folder_path = 'output'
    formatted_name = file_name if file_name.endswith('.html') else f'{file_name}.html'
    file_path = f'{folder_path}/{formatted_name}'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(file_path, 'w') as file:
        file.write(html_content)