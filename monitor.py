import subprocess
import time
import re

CONTAINER_NAME = "tenant_db"
INTERVAL = 1

cpu_values = []
memory_values = []

print("Monitoring PostgreSQL...")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        result = subprocess.run(
            [
                "docker", "stats", "--no-stream",
                "--format", "{{.CPUPerc}},{{.MemUsage}}",
                CONTAINER_NAME
            ],
            capture_output=True,
            text=True,
            check=True
        )

        values = result.stdout.strip().split(",")

        cpu = float(values[0].replace("%", ""))

        memory_text = values[1].split("/")[0].strip()
        memory = float(re.search(r"[\d.]+", memory_text).group())

        cpu_values.append(cpu)
        memory_values.append(memory)

        print(
            f"CPU: {cpu:.2f}% | "
            f"Memory: {memory:.2f} MiB"
        )

        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\n\nMonitoring stopped.")

    if cpu_values:
        print("\n===== POSTGRESQL RESOURCE SUMMARY =====")
        print(f"Samples collected: {len(cpu_values)}")
        print(f"Average CPU: {sum(cpu_values) / len(cpu_values):.2f}%")
        print(f"Peak CPU: {max(cpu_values):.2f}%")
        print(f"Average Memory: {sum(memory_values) / len(memory_values):.2f} MiB")
        print(f"Peak Memory: {max(memory_values):.2f} MiB")
        print("=======================================")