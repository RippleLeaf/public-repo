import time
import math

# nohup python3 keep_alive.py > keep_alive.log 2>&1 &

# Target CPU utilization percentage (e.g., 6%)
TARGET_UTILIZATION = 30.0  
# Time slice configuration for the calculation loop
INTERVAL = 0.1           

print(f"Starting keep-alive script. Target CPU: {TARGET_UTILIZATION}%")
print("Press Ctrl+C to stop.")

try:
    while True:
        start_time = time.perf_counter()
        
        # Calculate active work duration vs rest duration
        work_duration = INTERVAL * (TARGET_UTILIZATION / 100.0)
        rest_duration = INTERVAL - work_duration
        
        # Burn CPU cycles for the designated work window
        while (time.perf_counter() - start_time) < work_duration:
            # Simple math operation to consume CPU cycles
            _ = math.sqrt(99999.9)
            
        # Sleep for the remainder of the interval slice
        time.sleep(rest_duration)
        
except KeyboardInterrupt:
    print("\nScript stopped by user.")
