import kivy
from flask import Flask, request
from usb4a import usb
from usbserial4a import serial4a
from kivy.app import App
from kivy.uix.textinput import TextInput
from threading import Thread

port = "/dev/bus/usb/001/005"

device = usb.get_usb_device(port)
if not usb.has_usb_permission(device):
    usb.request_usb_permission(device)

ser = serial4a.get_serial_port(
    port,
    115200,
    8,
    "N",
    1,
    timeout=1
)

def ready_for_command():
    # is it OK to send a command? OD 
    cmd = b"\x0D"
    # print('Sending... Ping'+cmd)
    ser.write(cmd)
    # print('Receiving...Ping')
    out = ser.read()
    # print(list(out))
    if out == b"\x0D":
        # print('Received...Ping')
        return True
    else:
        # print('Not..Received...Ping')
        return False

def play_motion(motion_id):
    """
    plays the motion with id
    """
    motionhex = format(motion_id, '02X')
    # Send Command to play motion data 1
    CMD = b'\xF4'
    OPT = b'\x05'
    NUM = bytes.fromhex(motionhex)
    print(NUM)
    SUM = bytes.fromhex(format((0xF4 + 0x05 + motion_id) % 256, '02X'))
    DATA = (CMD + OPT + NUM + SUM)
    print('Sending... Commands')
    ready_for_command()
    ser.write(DATA)
    print('Receiving...Command Response')
    out = ser.read(1)
    if out == b"\x06":
        return True
    else:
        return False
play_motion(1)

class MyApp(App):
    
    host = '0.0.0.0'
    port = 5000

    def build(self):
        self.log_text = TextInput(multiline=True, text='Starting\n')
        Thread(target=self.start_flask).start()
        self.log_text.insert_text('Flask listening on %s:%s\n' % (self.host, self.port))
        return self.log_text

    def start_flask(self):
        self.flask_app = Flask(__name__)

        # Define your robot control function
        def play_motion_from_api(motion):
            # Here, you would implement the logic to control your robot based on the motion provided
            if motion == "move forward":
                play_motion(1)
                return "Robot moving forward"
            elif motion == "move backward":
                play_motion(23)
                return "Robot moving backward"
            elif motion == "turn left":
                play_motion(12)
                return "Robot turning left"
            elif motion == "turn right":
                play_motion(13)
                return "Robot turning right"
            elif motion == "bow":
                play_motion(2)
                return "Robot bowing"
            elif motion == "push ups":
                play_motion(3)
                return "Robot doing push ups"
            elif motion == "step left":
                play_motion(10)
                return "Robot stepped left"
            elif motion == "step right":
                play_motion(13)
                return "Robot stepped right"
            elif motion == "cartwheel right":
                play_motion(15)
                return "Robot cartwheel right"
            elif motion == "cartwheel left":
                play_motion(14)
                return "Robot cartwheel left"
            elif motion == "get up off belly":
                play_motion(9)
                return "Robot get up off belly"
            elif motion == "get up off back":
                play_motion(8)
                return "Robot get up off back"
            elif motion == "front roll":
                play_motion(16)
                return "Robot front roll"
            elif motion == "back roll":
                play_motion(17)
                return "Robot back roll"
            elif motion == "happy dance":
                play_motion(4)
                return "Robot happy dance"
            else:
                # Handle invalid motion
                return "Invalid motion"
# Define a route to handle motion requests
        @self.flask_app.route('/motion', methods=['POST'])
        def handle_motion():
            # Get the motion from the request
            motion = request.json.get('motion')
            # Call the play_motion function with the specified motion
            response = play_motion_from_api(motion)
            return f'Motion {motion} executed with {response}'

        self.flask_app.run(host=self.host, port=self.port)


if __name__ == '__main__':
    MyApp().run()