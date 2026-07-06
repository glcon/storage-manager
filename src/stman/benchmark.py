import time
import subprocess
import sys
from .dir_utils import dir_size_dll


def run_benchmark(path: str) -> None:
    '''
    Benchmarks stman's C++ DLL against PowerShell's Get-ChildItem
    for recursive directory size calculation.

    Args:
        path: The directory path to benchmark.

    Returns:
        None
    '''

    print(f"\nBenchmarking: {path}")
    print("─" * 50)

    # --- Warm the disk cache (run both once, discard results) ---
    print("Warming disk cache...", end="\r")
    dir_size_dll.get_directory_size(path)
    subprocess.run(
        ["powershell", "-Command",
         f"Get-ChildItem -Path '{path}' -Recurse -ErrorAction SilentlyContinue "
         f"| Measure-Object -Property Length -Sum"],
        capture_output=True, text=True
    )

    # --- Time stman ---
    start = time.perf_counter()
    dir_size_dll.get_directory_size(path)
    stman_time = time.perf_counter() - start

    # --- Time PowerShell ---
    start = time.perf_counter()
    subprocess.run(
        ["powershell", "-Command",
         f"Get-ChildItem -Path '{path}' -Recurse -ErrorAction SilentlyContinue "
         f"| Measure-Object -Property Length -Sum"],
        capture_output=True, text=True
    )
    ps_time = time.perf_counter() - start

    # --- Report ---
    speedup = ps_time / stman_time if stman_time > 0 else float("inf")

    print(f"  stman (C++ DLL):     {stman_time:.2f}s")
    print(f"  PowerShell GCI:      {ps_time:.2f}s")
    print(f"  Speedup:             {speedup:.1f}x")
    print("─" * 50)
    print()
