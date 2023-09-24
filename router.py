import os
import subprocess

def run_script(script_path):
    subprocess.run(['python', script_path])

if __name__ == '__main__':
    directory_path = './projects'
    subfolders = [f.path for f in os.scandir(directory_path) if f.is_dir()]
    scripts = [os.path.join(subfolder, 'script.py') for subfolder in subfolders]

    for i, script in enumerate(scripts, start=1):
        print(f"{i}. {os.path.basename(os.path.dirname(script))}")  # Display folder name

    try:
        choice = int(input("Which script do you want to run? (Enter the corresponding number): "))

        if 0 < choice <= len(scripts):
            run_script(scripts[choice-1])
        else:
            print("Invalid choice!")
    except ValueError:
        print("Please enter a valid number!")
