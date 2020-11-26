import os, sys
from src.main import MainWindow

# Si intentamos ejecutar como root
def check_if_run_as_root():
    if os.geteuid() == 0: # uid = 0 -> root
      os.sys.stderr.write('Error: no se puede ejecutar el programa como root! (ni deberías)\n')
      sys.exit(0)

def main():
  check_if_run_as_root()
  MainWindow()


if __name__ == "__main__":
    try:
      main()
    except KeyboardInterrupt:
      print("- Terminación forzada por el usuario -")
