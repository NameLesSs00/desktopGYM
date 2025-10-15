import os 
import subprocess

def covert_ui_files():
  ui_files = [f for f in os.listdir('.') if f.endswith(".ui")]
  if not ui_files:
    print("no ui files found")
    return
  for ui_file in ui_files:
    base_name = os.path.splitext(ui_file)[0]
    output_file = f"ui_{base_name}.py"

    try:
      subprocess.run(["pyside6-uic" , ui_file,"-o" , output_file], check=True)
      print(f"Convert {ui_file} to {output_file}")
    except FileNotFoundError:
      print("Error1")
      return
    except subprocess.CalledProcessError:
      print("error2")

if __name__ == "__main__":
  covert_ui_files()