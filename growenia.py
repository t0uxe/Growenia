import os
from src.controllers.main import MainWindow

# Si intentamos ejecutar como root
def check_if_run_as_root():
  try:
      uid = os.geteuid()
  except Exception:
      pass
  else:
      if uid == 0:
          os.sys.stderr.write('Error: no se puede ejecutar el programa como root! (ni deberías)\n')

def main():
  check_if_run_as_root()
  main_window = MainWindow()
  print("ola k ase")
  main_window.start()  


if __name__ == "__main__":
    try:
      main()
    except KeyboardInterrupt:
      print("- Terminación forzada por el usuario -")