import tkinter as tk
from tkinter import messagebox
import random
from hangman_wortliste import wortList

class HangmanGame:
    
    def createGridBackground(self):
        """Kareli defter görünümü için yatay ve dikey çizgiler oluşturur."""
        spacing = 20
        for i in range(0, 1000, spacing):
            self.hangman_canvas.create_line(0, i, 1000, i, fill="lightgrey")
        for i in range(0, 1000, spacing):
            self.hangman_canvas.create_line(i, 0, i, 1000, fill="lightgrey")

    def __init__(self, root, wortList, lives, difficulty="medium"):
        self.root = root
        self.lives = lives
        self.difficulty = difficulty
        self.gesamtLebens = lives
        self.wort = random.choice(wortList)
        self.richtigerBuchstabe = []
        self.gameOver = False
        self.hints_used = 0

        # GUI Elemanları
        self.label_lives = tk.Label(root, text=f"{self.lives} von {self.gesamtLebens} Leben übrig", 
                                  font=("Cascadia Code", 14), fg="red")
        self.label_lives.pack(side=tk.TOP)

        self.hangman_canvas = tk.Canvas(root, width=600, height=600)
        self.hangman_canvas.pack()
        self.createGridBackground()

        self.display = ["_"] * len(self.wort)
        self.label_wort = tk.Label(root, text=" ".join(self.display), 
                                 font=("Cascadia Code", 24))
        self.label_wort.pack()

        # Fare tıklama özelliği ekleme
        self.hangman_canvas.bind("<Button-1>", self.canvas_click)

        # Harf butonları
        self.buchstaben_frame = tk.Frame(root)
        self.buchstaben_frame.pack()
        self.create_keyboard()

        self.button_hint = tk.Button(root, text="Hinweis", command=self.useHint)
        self.button_hint.pack()

        self.updateHangmanCanvas()

    def canvas_click(self, event):
        """Fare tıklamasını işleme"""
        if not self.gameOver:
            x, y = event.x, event.y
            # Tıklanan alan kontrolü (örneğin belirli bir bölge)
            if 50 <= x <= 300 and 50 <= y <= 350:
                self.useHint()

    def create_keyboard(self):
        """Klavye butonlarını oluştur"""
        keyboard = [
            "qwertzuiopü",
            "asdfghjklöä",
            "yxcvbnm"
        ]
        
        for row_idx, row in enumerate(keyboard):
            row_frame = tk.Frame(self.buchstaben_frame)
            row_frame.pack()
            for char in row:
                btn = tk.Button(row_frame, text=char.upper(), width=3, height=2,
                               command=lambda c=char: self.rate_buchstabe_click(c))
                btn.pack(side=tk.LEFT, padx=2, pady=2)
                setattr(self, f"btn_{char}", btn)

    def rate_buchstabe_click(self, char):
        """Buton tıklamasıyla harf tahmini"""
        if not self.gameOver and char not in self.richtigerBuchstabe:
            self.rate_buchstabe(char)

    def rate_buchstabe(self, erraten):
        """Harf tahmini işlemi"""
        if erraten in self.richtigerBuchstabe:
            messagebox.showinfo("Schon geraten", f"Sie haben '{erraten}' bereits geraten.")
            return

        self.richtigerBuchstabe.append(erraten)
        btn = getattr(self, f"btn_{erraten}", None)
        if btn:
            btn.config(state=tk.DISABLED)

        if erraten in self.wort:
            self.updateDisplay(erraten)
            if btn:
                btn.config(bg="lightgreen")
        else:
            self.verlierLeben()
            if btn:
                btn.config(bg="salmon")

        if self.istSpielGewonnen():
            self.gameOver = True
            messagebox.showinfo("Gewonnen :)", "Herzlichen Glückwunsch!")
            self.askReplay()
        elif self.istSpielVerloren():
            self.gameOver = True
            messagebox.showinfo("Verloren :(", f"Das Wort war: '{self.wort}'")
            self.askReplay()

        self.updateHangmanCanvas()

    def askReplay(self):
        """Yeniden oynama ve zorluk seçimi"""
        antwort = messagebox.askyesno("Spiel beenden", "Möchten Sie nochmal spielen?")
        if antwort:
            self.show_difficulty_selection()
        else:
            self.root.quit()

    def show_difficulty_selection(self):
        """Zorluk seçim penceresi"""
        diff_window = tk.Toplevel(self.root)
        diff_window.title("Schwierigkeitsgrad")
        
        tk.Label(diff_window, text="Wählen Sie den Schwierigkeitsgrad:", 
                font=("Cascadia Code", 14)).pack(pady=10)
        
        difficulty = tk.StringVar(value=self.difficulty)
        
        modes = [("Einfach (15 Leben)", "einfach"),
                ("Mittel (10 Leben)", "mittel"),
                ("Schwer (5 Leben)", "schwer")]
        
        for text, mode in modes:
            tk.Radiobutton(diff_window, text=text, variable=difficulty, 
                          value=mode, font=("Cascadia Code", 12)).pack(anchor=tk.W)
        
        tk.Button(diff_window, text="Starten", 
                command=lambda: self.resetGame(difficulty.get()),
                font=("Cascadia Code", 14)).pack(pady=10)

    def resetGame(self, difficulty):
        """Oyunu belirtilen zorlukta sıfırla"""
        self.difficulty = difficulty
        if difficulty == "einfach":
            self.lives = 15
        elif difficulty == "schwer":
            self.lives = 5
        else:
            self.lives = 10
            
        self.gesamtLebens = self.lives
        self.wort = random.choice(wortList)
        self.display = ["_"] * len(self.wort)
        self.richtigerBuchstabe = []
        self.gameOver = False
        self.hints_used = 0
        
        # GUI'yi güncelle
        self.label_wort.config(text=" ".join(self.display))
        self.label_lives.config(text=f"{self.lives} von {self.gesamtLebens} Leben übrig")
        
        # Klavyeyi sıfırla
        for char in "qwertzuiopüasdfghjklöäyxcvbnm":
            btn = getattr(self, f"btn_{char}", None)
            if btn:
                btn.config(state=tk.NORMAL, bg="SystemButtonFace")
        
        self.updateHangmanCanvas()

    # Diğer fonksiyonlar (updateDisplay, verlierLeben, etc.) aynı kalacak
    # ...

def start_game():
    root = tk.Tk()
    root.title("Hangman Spiel")
    game = HangmanGame(root, wortList, lives=10)  # Varsayılan orta zorluk
    root.mainloop()

if __name__ == "__main__":
    start_game()