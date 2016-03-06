from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.audio import SoundLoader
from game_data import GameData
from kivy.uix.textinput import TextInput
import threading

#returns data per level
class LevelData():
    def __init__(self):
        self.level_data = GameData()

    def get_task(self):
        data = self.level_data.get_level_data()
        return {'image': data.image, 
                'answers': data.answers, 
                'data_id': data.data_id
                }

#declare Menu Screen
class MenuScreen(Screen):
    sound = SoundLoader.load("sounds/click.ogg")
    background = SoundLoader.load("sounds/background.ogg")
    background.loop = True
    background.volume = 0.09
    background.play()

    def click_sound(self):        
        self.sound.play()
    
#declare Level Screen
class LevelScreen(Screen):
    game_data = GameData()
    #get user current level
    user_level = game_data.read_data('user.json')
    
    def set_next_level(self):
        self.get_level_data()
        self.user_answers = []
        self.ids.feedback.text = ''
        self.ids.user_answers.text = ''
        self.ids.level.text = 'Level ' + str(self.user_level) 
        self.ids.answer.text = 'Answers: ' + str(self.answers)
        self.sound(self.load_sounds)
    
    def buttonClicked(self,btn):
        self.user_answer = self.ids.user_answer.text.lower()
        if self.user_answer:
            if self.user_answer in self.answers:
                if self.user_answer not in self.user_answers:
                    self.ids.feedback.text = 'Correct!'
    
                    self.sound(self.correct_sound)
                    self.user_answers.append(self.user_answer)
                    self.ids.user_answers.text = ', '.join(self.user_answers)
                    
                    if len(self.user_answers) == 3:
                        self.ids.feedback.text = 'Got 6!'
                        
                        self.update_data(self.user_level,self.task_values['data_id'])
                        
                        
                        if len(self.game_data.level_data) <= self.user_level:
                            print len(self.game_data.level_data), self.user_level
                            self.manager.current = 'update_screen'
                        self.user_level += 1
                        self.set_next_level()
                        
                else:
                    self.ids.feedback.text = 'Answer already in the list'
                    self.sound(self.wrong_sound)
            else:
                self.ids.feedback.text = 'Wrong!'
                self.sound(self.wrong_sound)
        
        self.ids.user_answer.text = ''

    def get_level_data(self):
        self.Tasks = LevelData()
        self.task_values = self.Tasks.get_task()
        self.ids.image.source = self.task_values['image']
        self.answers = self.task_values['answers']

    def update_data(self,user_level,data_id):
        game_data = self.game_data
        game_data.store_data(user_level, 'user.json')
        game_data.store_data(data_id, 'levels_completed.json')

    def sound(self, target=None):
        t1 = threading.Thread(target=target)
        t1.start()

    def load_sounds(self):
        self.sounds = {'correct': SoundLoader.load("sounds/correct.ogg"),
                        'wrong': SoundLoader.load("sounds/wrong.ogg")}

    def correct_sound(self):
        self.sounds['correct'].play()

    def wrong_sound(self):
        self.sounds['wrong'].play()

#declare Update Screen
class UpdateScreen(Screen):
    sound = SoundLoader.load("sounds/click.ogg")

    def click_sound(self):
        self.sound.play()

class Got6WordsApp(App):
    layout = ScreenManager(transition=FadeTransition())
    def build(self):
        self.layout.add_widget(MenuScreen(name='menu_screen'))
        self.layout.add_widget(LevelScreen(name='level_screen'))
        self.layout.add_widget(UpdateScreen(name='update_screen'))
        return self.layout
    
if __name__ == '__main__':
    Got6WordsApp().run()
