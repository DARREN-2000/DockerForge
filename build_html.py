import os
import json

def get_python_files(directory):
    files_dict = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                with open(full_path, 'r', encoding='utf-8') as f:
                    rel_path = os.path.relpath(full_path, 'src')
                    files_dict[rel_path] = f.read()
    return files_dict

python_files = get_python_files('src/dockerforge')
python_files_json = json.dumps(python_files)

# We load the template from a separate file to avoid f-string escaping issues
with open('template.html', 'r', encoding='utf-8') as f:
    template = f.read()

final_html = template.replace('__VFS_FILES_JSON_INJECTION__', python_files_json)

if not os.path.exists('docs'):
    os.makedirs('docs')

with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)
print("Playground HTML generated at docs/index.html")
