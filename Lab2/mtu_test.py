import subprocess
import sys
import platform
import re


def check_if_host_is_reachable(host):
    try:
        if platform.system().lower() == 'windows':
            command = ['ping', '-n', '5', host]
        else:
            command = ['ping', '-c', '5', host]

        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        return result.returncode == 0
    except Exception as e:
        return False


def check_ping(host, mtu):
    package_size = mtu - 28  # account for headers size
    try:
        if platform.system().lower() == 'windows':
            command = ['ping', '-n', '1', '-f', '-l', str(package_size), host]
        else:
            command = ['ping', '-c', '1', '-s', str(package_size), host]

        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        return result.returncode == 0
    except Exception as e:
        return False


def find_min_mtu(host):
    low = 28  # headers size
    high = 3000  # default max MTU * 2

    while low + 1 < high:
        print('.', end='', flush=True)

        mid = (low + high) // 2
        if check_ping(host, mid):
            low = mid
        else:
            high = mid

    return low


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: docker build -t mtu_test .\n       docker run --rm mtu_test <destination_host>")
        sys.exit(1)

    host = sys.argv[1]

    # Naive regex validation
    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        print("Invalid host argument")
        sys.exit(1)

    if not check_if_host_is_reachable(host):
        print(f"Host {host} is not reachable")
        sys.exit(1)

    print(f"Doing MTU test", end='')
    mtu = find_min_mtu(host)
    print(f"\nMinimum MTU for {host}: {mtu}")


if __name__ == "__main__":
    main()
