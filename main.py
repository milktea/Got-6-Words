from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.audio import SoundLoader
from game_data import GameData
from kivy.uix.textinput import TextInput
import threading
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock



# Basic class Menu Screen Layout
class MenuScreen(Screen):
    sound = SoundLoader.load("sounds/click.ogg")
    background = SoundLoader.load("sounds/background.ogg")
    background.loop = True
    background.volume = 0.09
    background.play()

    def click_sound(self):
        self.sound.play()

# Basic class Level Screen Layout

class LevelScreen(Screen):
    game_data = GameData()
    user_level = game_data.read_data('user.json')

    def set_next_level(self):
        try:
            if len(self.game_data.level_data) < self.user_level:
                #self.manager.current = 'update_screen'
                self.pop_up()
            else:
                self.get_level_data()
                self.user_answers = []
                self.ids.feedback.text = ''
                self.ids.user_answers.text = ''
                self.ids.level.text = 'Level ' + str(self.user_level)
                #self.ids.answer.text = 'Answers: ' + str(self.answers)
                self.sound(self.load_sounds)
        #no more game data; all levels completed    
        except AttributeError:
            self.pop_up()
            
    def pop_up(self):
        pop = Popup(title='Updating', content=Label(text='Update'), auto_dismiss=False)
        pop.open()
        # Clock.schedule_once(self.update, 0)
        # pop.dismiss()

    def get_level_data(self):
            self.level_data = self.game_data.get_level_data()
            self.ids.image.source = self.level_data.image
            self.answers = self.level_data.answers
        
    def buttonClicked(self, btn):
        self.check_answer()
        if len(self.user_answers) == 6:
            self.level_completed()

        #sets input field to null everytime button is clicked
        self.ids.user_answer.text = ''

    def check_answer(self):
        self.user_answer = self.ids.user_answer.text.lower()
        if self.user_answer:
            if self.user_answer in self.answers:
                if self.user_answer not in self.user_answers:
                    self.correct_answer()
                else:
                    self.answer_in_list()
            else:
                self.wrong_answer()
            
    def correct_answer(self):
        self.ids.feedback.text = 'Correct!'
        self.sound(self.correct_sound)
        self.user_answers.append(self.user_answer)
        self.ids.user_answers.text = ', '.join(self.user_answers)

    def wrong_answer(self):
        self.ids.feedback.text = 'Wrong!'
        self.sound(self.wrong_sound)

    def answer_in_list(self):
        self.ids.feedback.text = 'Answer already in the list'
        self.sound(self.wrong_sound)

    def level_completed(self):
        self.ids.feedback.text = 'Got 6!'
        self.user_level += 1
        self.update_data(self.user_level, self.level_data.data_id)
        self.set_next_level()

    # Stores data (Json files)
    def update_data(self, user_level, data_id):
        game_data = self.game_data
        game_data.store_data(user_level, 'user.json')
        game_data.store_data(data_id, 'levels_completed.json')

    def sound(self, target=None):
        t1 = threading.Thread(target=target)
        t1.start()

    def load_sounds(self):
        self.sounds = {
            'correct': SoundLoader.load("sounds/correct.ogg"),
            'wrong': SoundLoader.load("sounds/wrong.ogg")}

    def correct_sound(self):
        self.sounds['correct'].play()

    def wrong_sound(self):
        self.sounds['wrong'].play()


# Basic class Update Screen Layout
class UpdateScreen(Screen):
    sound = SoundLoader.load("sounds/click.ogg")

    def click_sound(self):
        self.sound.play()


# Main App Class
class Got6WordsApp(App):
    layout = ScreenManager(transition=FadeTransition())

    def build(self):
        self.layout.add_widget(MenuScreen(name='menu_screen'))
        self.layout.add_widget(LevelScreen(name='level_screen'))
        self.layout.add_widget(UpdateScreen(name='update_screen'))
        return self.layout

# Main Program
if __name__ == '__main__':
    Got6WordsApp().run()

