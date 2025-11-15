# Setup

1. connect arduino board (connected to sensor) to the machine.

1. move to this directory via bash and activate virtual environment.
    ```bash
    cd ~/media-control
    source .venv/bin/activate
    ```
    - if venv doesn't exit, then:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

1. verify serial device.
    ```bash
    ls /dev/ttyUSB*  # /dev/ttyUSB0
    ```

1. run python script
    ```bash
    cd ~/media-control/python
    python3 gesture_control_continuous_v2.py
    ```

    - Keep VLC open before this and focus that window after running python script.
    - gestures will start working right away.

1. to quit python script
    ```bash
    ctrl + c
    ```

1. exit venv
    ```bash
    deactivate
    ```

1. unplug the arduino
1. close the terminal

# Upload another sketch to arduino

```bash
arduino-cli compile --fqbn arduino:avr:uno ~/media-control/arduino/SingleSensor
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno ~/media-control/arduino/SingleSensor
```

# Reference
[study from here](https://chatgpt.com/share/6917d4fe-ac4c-8002-b581-eb6d1e19a3a4)