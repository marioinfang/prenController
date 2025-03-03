from communication.uart_handler import UARTHandler
from state_machine.state_machine import CarStateMachine

if __name__ == "__main__":
    uart = UARTHandler("some/port", 115200, 2)
    fsm = CarStateMachine(uart)
    fsm.run()