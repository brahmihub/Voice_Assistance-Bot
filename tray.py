from pystray import Icon, Menu, MenuItem as PyMenuItem
from PIL import Image
import threading
import app

class MyApplication:

    def __init__(self):
        # Create the system tray icon
        self.image = Image.open("red_icon.jpg")
        self.icon = Icon("my_icon", self.image, "Echo")

        # Create a menu for the system tray
        self.voice_submenu = (
            PyMenuItem('Male', self.set_voice),
            PyMenuItem('Female', self.set_voice),
            # Add more voice options as needed
        )

        self.language_submenu = (
            PyMenuItem('english', self.set_language),
            PyMenuItem('arabic', self.set_language),
            PyMenuItem('spanish', self.set_language),
            PyMenuItem('italian', self.set_language),
            # Add more language options as needed
        )

        self.main_menu = (
            PyMenuItem('Turn On', self.program),
            PyMenuItem('Voice', Menu(*self.voice_submenu)),
            PyMenuItem('Language', Menu(*self.language_submenu)),
            PyMenuItem('Exit', self.quit),
        )

        self.icon.menu = Menu(*self.main_menu)

        # Display the system tray icon
        self.icon.run()

    def program(self, icon, item):
        if app.exit_flag is False:
            app.exit_flag = True
            program_thread = threading.Thread(target=app.main)
            program_thread.start()
            self.icon.icon = Image.open("green_icon.jpg")
            self.update_main_menu('Turn Off')
        else:
            app.exit_flag = False
            self.icon.icon = Image.open("red_icon.jpg")
            self.update_main_menu('Turn On')

    def update_main_menu(self, turn_state):
        # Create a new instance of Menu with updated items
        new_menu = (
            PyMenuItem(turn_state, self.program),
            PyMenuItem('Voice', Menu(*self.voice_submenu)),
            PyMenuItem('Language', Menu(*self.language_submenu)),
            PyMenuItem('Exit', self.quit),
        )
        self.icon.menu = Menu(*new_menu)

    def set_language(self, icon, item):
        print("Language set to", item.text)
        
    def set_voice(self, icon, item):
        print("Voice set to", item.text)

    def quit(self, icon, item):
        icon.stop()

if __name__ == "__main__":
    app = MyApplication()
