# clean_obj.py
def clean_obj_file(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            if line.startswith('usemtl') or line.startswith('mtllib'):
                continue  # Skip material lines
            if line.startswith('f '):
                # Ensure face definitions are correctly formatted
                parts = line.strip().split()[1:]
                cleaned_parts = []
                for part in parts:
                    indices = part.split('/')
                    cleaned_indices = [index if index else '0' for index in indices]
                    cleaned_parts.append('/'.join(cleaned_indices))
                cleaned_line = 'f ' + ' '.join(cleaned_parts) + '\n'
                outfile.write(cleaned_line)
            else:
                outfile.write(line)

clean_obj_file("models/omentest.obj", "models/pepe.obj")