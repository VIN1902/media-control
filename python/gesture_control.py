import serial, time, pyautogui, statistics, sys

# ---------------- user settings ----------------
PORT = "/dev/ttyUSB0"
BAUD = 115200

# distance thresholds (tune these to taste)
PAUSE_MAX = 15      # ≤ 15 cm  -> play/pause
VOL_UP_MAX = 35     # 15–35 cm -> volume up
# > 35 cm -> volume down
SMOOTH_WINDOW = 5   # number of samples for smoothing
COOLDOWN_SEC = 1.0  # time between actions
# ------------------------------------------------

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
    last_state = "idle"
    last_action_time = 0

    print("Running... (near=play/pause, mid=vol up, far=vol down)")
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

            # decide which zone the hand is in
            if smooth <= PAUSE_MAX:
                state = "pause"
            elif smooth <= VOL_UP_MAX:
                state = "up"
            else:
                state = "down"

            print(f"\rDistance:{smooth:5.1f} cm  Zone:{state:>5}", end="")

            # only trigger on state change + cooldown
            if state != last_state and now - last_action_time >= COOLDOWN_SEC:
                print("")  # newline for log
                if state == "pause":
                    print("Action: PLAY/PAUSE")
                    pyautogui.press("space")
                elif state == "up":
                    print("Action: VOLUME UP")
                    pyautogui.hotkey("ctrl", "up")
                elif state == "down":
                    print("Action: VOLUME DOWN")
                    pyautogui.hotkey("ctrl", "down")
                last_action_time = now
                last_state = state

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print("\nError:", e)
            time.sleep(0.5)

if __name__ == "__main__":
    main()
