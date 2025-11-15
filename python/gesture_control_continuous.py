#!/usr/bin/env python3
import serial, time, pyautogui, statistics, sys

PORT = "/dev/ttyUSB0"
BAUD = 115200
SMOOTH_WINDOW = 5      # number of samples to smooth distance
COOLDOWN_PAUSE = 1.0   # time between play/pause triggers (seconds)
NEAR_PAUSE = 10        # ≤ 10 cm triggers play/pause
STEP_DELAY = 0.15      # how often to check movement for volume adjust
DELTA_THRESHOLD = 1.0  # minimum cm change to count as movement

def median_filter(buf, new):
    buf.append(new)
    if len(buf) > SMOOTH_WINDOW:
        buf.pop(0)
    return statistics.median(buf)

def main():
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        print(f"Connected to {PORT}")
    except Exception as e:
        print("Error opening serial port:", e)
        sys.exit(1)

    smooth_buf = []
    last_dist = None
    last_pause_time = 0
    last_vol_time = 0

    print("Continuous gesture mode:")
    print(" - Move hand away to increase volume")
    print(" - Move hand closer to decrease volume")
    print(" - Hold hand very close (≤10 cm) to play/pause")

    while True:
        try:
            line = ser.readline().decode(errors="ignore").strip()
            if not line.startswith("Dist:"):
                continue
            dist = float(line.split(":")[1])
            if dist <= 0:
                continue

            smooth = median_filter(smooth_buf, dist)
            now = time.time()

            if smooth <= NEAR_PAUSE and now - last_pause_time > COOLDOWN_PAUSE:
                print(f"\nPlay/Pause triggered (dist={smooth:.1f}cm)")
                pyautogui.press("space")
                last_pause_time = now
                continue

            if last_dist is not None and now - last_vol_time > STEP_DELAY:
                delta = smooth - last_dist

                if abs(delta) >= DELTA_THRESHOLD:
                    # reversed logic here
                    direction = "up" if delta > 0 else "down"
                    print(f"\rDistance:{smooth:5.1f}cm Δ{delta:+4.1f} -> Volume {direction}   ", end="")
                    if direction == "up":
                        pyautogui.hotkey("ctrl", "up")
                    else:
                        pyautogui.hotkey("ctrl", "down")
                    last_vol_time = now

            last_dist = smooth

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print("\nError:", e)
            time.sleep(0.5)

if __name__ == "__main__":
    main()
