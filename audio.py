import pyttsx3 as th
import threading
import time

class audiof:
    def __init__(self, voice='male', speakstatus=True):
        self.voice = voice
        self.speakstatus = speakstatus
        self.words = {
            '1': 'one',
            '2': 'two',
            '3': 'three',
            '4': 'four',
            '5': 'five',
            '6': 'six',
            '7': 'seven',
            '8': 'eight',
            '9': 'nine',
            '0': 'zero',
            '+': 'plus',
            '-': 'minus',
            'x': 'multiply',
            '/': 'divide',
            '=': 'equals to',
            '.': 'point',
            ',': 'comma',
            '√': 'square root',
            '^': 'power',
            'x!': 'factorial',
            'rad': 'radians',
            'x°': 'degrees',
            'sin(x)': 'sine',
            'cos(x)': 'cosine',
            'tan(x)': 'tangent',
            'ln': 'natural log',
            'e^x': 'exponential',
            'π': 'pi',
            'e': 'Eulers number',
            '<--': 'back',
            'AC': 'All clear',
            'Audio mode enabled': 'Audio mode enabled',
            'Audio mode disabled': 'Audio mode disabled',
            'Scientific mode enabled': 'Scientific mode enabled',
            'Scientific mode disabled': 'Scientific mode disabled'
        }
        
        # Initialize TTS engine
        self.engine = th.init()
        v = self.engine.getProperty('voices')
        if v:
            self.engine.setProperty('voice', v[0].id)
        
        # Use a lock to prevent concurrent access
        self.lock = threading.Lock()
    
    def speak(self, context):
        """Speak text using threading with lock"""
        if self.speakstatus:
            # Get the text to speak
            text_to_speak = self.words.get(context, context)
            
            # Create and start thread
            thread = threading.Thread(target=self._speak_with_lock, args=(text_to_speak,), daemon=True)
            thread.start()
    
    def _speak_with_lock(self, text):
        """Internal method to speak with thread lock"""
        with self.lock:
            try:
                # Create a new engine instance for this thread
                engine = th.init()
                v = engine.getProperty('voices')
                if v:
                    engine.setProperty('voice', v[0].id)
                
                engine.say(text)
                engine.runAndWait()
                engine.stop()
            except Exception as e:
                print(f"Audio error: {e}")


if __name__ == '__main__':
    ob = audiof()
    ob.speak('=')
    time.sleep(2)  # Give it time to speak