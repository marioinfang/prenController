from state_machine import StateMachine

if __name__ == "__main__":
    current_state = StateMachine()

    for _ in range (20):
        current_state.change()
