import os
import time

import pygame

from utils.log_config import get_logger

logger = get_logger(__name__)


def play_target_reached():
    play_sound("audio/target_reached.mp3")

def play_sound(file_path):
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return

    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()

    logger.error(f"Playing: {file_path}")
    while pygame.mixer.music.get_busy():
        time.sleep(1)