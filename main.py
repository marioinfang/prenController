from communication.uart_handler import UARThandler
from state_machine.state_machine import FahrzeugStateMachine

if __name__ == "__main__":
    uart = UARThandler()
    fsm = FahrzeugStateMachine(uart)
    fsm.run()