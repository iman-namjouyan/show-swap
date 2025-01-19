import os

def get_processes_using_swap():
    processes_using_swap = []

    for pid in os.listdir('/proc'):
        if pid.isdigit():
            try:
                smaps_file = '/proc/{0}/smaps'.format(pid)
                swap_used = 0

                with open(smaps_file, 'r') as file:
                    for line in file:
                        if line.startswith('Swap:'):
                            swap_used += int(line.split()[1])

                if swap_used > 0:
                    cmdline_file = '/proc/{0}/cmdline'.format(pid)
                    with open(cmdline_file, 'r') as file:
                        cmdline = file.read().replace('\x00', ' ').strip()
                    
                    processes_using_swap.append((pid, cmdline, swap_used))
            except (IOError, OSError):
                continue

    return processes_using_swap


if __name__ == '__main__':
    processes = get_processes_using_swap()
    if processes:
      
        processes = sorted(processes, key=lambda x: x[2], reverse=True)
        
        print("{0:<10}{1:<50}{2:<10}".format('PID', 'Command', 'Swap (KB)'))
        print("-" * 70)
        for pid, cmdline, swap_used in processes:
            print("{0:<10}{1:<50}{2:<10}".format(pid, cmdline, swap_used))
    else:
        print("No process uses swap...!!!")
