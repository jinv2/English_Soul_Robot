import os

# Get the script's directory and the project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
# Source and output now point to ui_frontend/assets for Netlify compatibility
assets_dir = os.path.join(project_root, 'ui_frontend', 'assets')

def escape_js(content):
    # Escape backslashes first, then backticks, and also dollar signs for template literal safety
    return content.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')

# Map variable names to filenames found in the assets directory
files = {
    'novelData': '《碗底青》小说.txt',
    'lyricsData': '碗底青歌词.txt'
}

js_content = ""
for var_name, filename in files.items():
    path = os.path.join(assets_dir, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            escaped_content = escape_js(content)
            js_content += f"const {var_name} = `{escaped_content}`;\n"
            print(f"Processed {filename} -> {var_name}")
    else:
        # Fallback for small variations in naming if necessary
        alternative_name = filename.replace('》小说', '》 小说')
        alt_path = os.path.join(assets_dir, alternative_name)
        if os.path.exists(alt_path):
            with open(alt_path, 'r', encoding='utf-8') as f:
                content = f.read()
                escaped_content = escape_js(content)
                js_content += f"const {var_name} = `{escaped_content}`;\n"
                print(f"Processed {alternative_name} (alt) -> {var_name}")
        else:
            print(f"Error: Could not find {filename} or {alternative_name} in {assets_dir}")

output_path = os.path.join(assets_dir, 'shensist_data.js')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Successfully generated: {output_path}")
