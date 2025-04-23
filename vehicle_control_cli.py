import cmd
from vehicle_control.vehicle_control_service import VehicleControlService
from state_machine.types.decision_state import Decision
from vehicle_control.types.detection_type import StopTypes
from vehicle_control.types.direction_type import DirectionType

class VehicleControlCLI(cmd.Cmd):
    intro = "🚗 Vehicle Control CLI - type 'help' to list commands.\n"
    prompt = "vehicle> "

    def __init__(self):
        super().__init__()
        self.service = VehicleControlService()

    def do_drive(self, arg):
        "drive <state:int> <blocked:bool> <distance:int> — Send drive command"
        try:
            args = arg.split()
            state = Decision(int(args[0]))
            blocked = args[1].lower() in ['true', '1', 'yes']
            distance = int(args[2])
            self.service.drive(state, blocked, distance)
            print("✅ Drive command sent.")
        except Exception as e:
            print(f"❌ Error: {e}")

    def do_stop(self, arg):
        "stop <state:int> <reason:int> — Send stop command with reason (1=WAYPOINT, 2=CONE, 3=OBSTACLE, 4=PATH)"
        try:
            args = arg.split()
            state = Decision(int(args[0]))
            reason = StopTypes(int(args[1]))
            self.service.stop(state, reason)
            print("✅ Stop command sent.")
        except Exception as e:
            print(f"❌ Error: {e}")

    def do_rotate(self, arg):
        "rotate <state:int> <direction:0|1> <angle:int> — Send rotate command (0=LEFT, 1=RIGHT)"
        try:
            args = arg.split()
            state = Decision(int(args[0]))
            direction = DirectionType(int(args[1]))
            angle = int(args[2])
            self.service.rotate(state, direction, angle)
            print("✅ Rotate command sent.")
        except Exception as e:
            print(f"❌ Error: {e}")

    def do_waypoint(self, arg):
        "waypoint <state:int> — Drive to waypoint"
        try:
            state = Decision(int(arg.strip()))
            self.service.drive_to_waypoint(state)
            print("✅ Drive to waypoint command sent.")
        except Exception as e:
            print(f"❌ Error: {e}")

    def do_listen(self, _):
        "listen — Start UART listening mode"
        self.service.start_listen()
        print("🟢 Listening started...")

    def do_unlisten(self, _):
        "unlisten — Stop UART listening mode"
        self.service.stop_listen()
        print("🔴 Listening stopped.")

    def do_recv(self, _):
        "recv — Get latest UART message"
        msg = self.service.get_received_message()
        if msg:
            print(f"📨 Received: {msg}")
        else:
            print("⏳ No message received.")

    def do_exit(self, _):
        "exit — Exit the CLI"
        print("👋 Exiting.")
        return True

    def do_help(self, arg):
        super().do_help(arg)
        print("\n🔁 Examples:")
        print("  drive 3 false 100 | drive <state:int> <blocked:bool> <distance:int> — Send drive command")
        print("  stop 3 3 | stop <state:int> <reason:int> — Send stop command with reason (1=WAYPOINT, 2=CONE, 3=OBSTACLE, 4=PATH)")
        print("  rotate 3 0 90 | rotate <state:int> <direction:0|1> <angle:int> — Send rotate command (0=LEFT, 1=RIGHT)")
        print("  waypoint 3 | to_waypoint <state:int> — Drive to waypoint")

if __name__ == '__main__':
    VehicleControlCLI().cmdloop()