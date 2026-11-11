import subprocess
import platform
def check_device(ip_address):
  system = platform.system().lower()
  count_option = "-n" if system == "windows" else "-c"
  result = subprocess.run(
  ["ping", count_option, "1", ip_address],
  capture_output=True,
  text=True,
  timeout=10
  )
  if result.returncode ==0:
    print(f"{ip_address} is online")
  else:
    print(f"{ip_address} is offline or not responding")

if  __name__ =="__main__":
  print ("network Monitoring Tool")
  check_device("8.8.8.8")
  check_device("1.1.1.1")
  check_device("9.9.9.9")
