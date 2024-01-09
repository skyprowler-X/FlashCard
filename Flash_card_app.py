from tkinter import *
import random as r
import pandas as pd
import time
from tkinter import messagebox


words_list = []
BG_COLOR = "#B1DDC6"
current_word = None
start = True


# ===============================Function Sections=================================
# def know_coords(click_event):
#     x = click_event.x
#     y = click_event.y
#     #print(f"X = {x}\nY = {y}\nFinished")


def change_canva_and_word():
    canva.itemconfig(canva_img, image=img_back_card)
    canva.itemconfig(canva_text_lang, text="English", fill="white")
    canva.itemconfig(canva_text_word, text=current_word[1], fill="white")


def change_word():
    global current_word, after_time
    canva.after_cancel(after_time)
    if len(words_list) > 1:
        random_number = r.randint(1, len(words_list) - 1)
        canva.itemconfig(canva_img, image=img_front_card)
        words_tpl = [tpl for tpl in words_list[random_number].items()][0]
        current_word = words_tpl
        canva.itemconfig(canva_text_word, text=words_tpl[0], fill="black")
        canva.itemconfig(canva_text_lang, text="French", fill="black")
        after_time = canva.after(3000, change_canva_and_word)
    else:
        messagebox.showinfo(
            title="YOU DID IT!",
            message="There's no more words to practices with. Take a rest 😁")
        words_data = pd.read_csv(r"Day - 31\Day 31 - Project\Practice_vocabulary.csv")

        if words_data.empty is not True and "practice" in words_list[0].values():
            empty_dt = pd.DataFrame()
            empty_dt.to_csv(
                r"Day - 31\Day 31 - Project\Practice_vocabulary.csv", index=False
            )


def remove_words_from_list(button):
    global current_word
    for words_dict in words_list:
        if current_word[0] in words_dict:
            words_list.remove(words_dict)
            break
        else:
            new_dict = {"French": [current_word[0]], "English": [current_word[1]]}
            if button == "fail":
                practice_data = pd.DataFrame(new_dict)
                print(practice_data)
                try:
                    data = pd.read_csv(
                        r"Day - 31\Day 31 - Project\Practice_vocabulary.csv"
                    )

                except Exception as e:
                    print(e)
                    practice_data.to_csv(
                        r"Day - 31\Day 31 - Project\Practice_vocabulary.csv",
                        index=False,
                    )

                else:
                    update_data = pd.concat([practice_data, data], ignore_index=True)
                    update_data.to_csv(
                        r"Day - 31\Day 31 - Project\Practice_vocabulary.csv",
                        index=False,
                    )
                break


# ================================Retrieve Data ====================================


try:
    words_data = pd.read_csv(r"Day - 31\Day 31 - Project\Practice_vocabulary.csv")
    if words_data.empty:
        raise Exception()

except Exception as e:
    print(e)
    words_data = pd.read_csv(r"Day - 31\Day 31 - Project\French_vocabulary.csv")
    words_with_columns = words_data.to_dict(orient="records")
    words_list = [{word["French"]: word["English"]} for word in words_with_columns]
    words_list.insert(0, {"source": "total_vocabulary"})
else:
    words_with_columns = words_data.to_dict(orient="records")
    words_list = [{word["French"]: word["English"]} for word in words_with_columns]
    words_list.insert(0, {"source": "practice"})


# =============================GUI section ==============================


root = Tk()
root.geometry("800x600")
root.title("Flash Card App")
root.config(bg=BG_COLOR, padx=50, pady=50)
# root.bind("<Button-1>", know_coords)

img_front_card = PhotoImage(file=r"Day - 31\Day 31 - Project\card_front_resized.png")
img_back_card = PhotoImage(file=r"Day - 31\Day 31 - Project\card_back_resized.png")
canva = Canvas(width=700, height=400)

canva_img = canva.create_image(360, 200, image=img_front_card)
canva_text_lang = canva.create_text(
    360, 86, text="Start", fill="black", font=("Ariel", 40, "italic")
)
canva_text_word = canva.create_text(355, 192, fill="black", font=("Ariel", 60, "bold"))

canva.grid(row=0, column=0, columnspan=2)
canva.config(bg=BG_COLOR, highlightbackground=BG_COLOR)
after_time = canva.after(3000, change_canva_and_word)

img_failed_button = PhotoImage(file=r"Day - 31\Day 31 - Project\wrong.png")
failed_button = Button(
    image=img_failed_button,
    command=lambda: (remove_words_from_list("fail"), change_word()),
)
failed_button.grid(row=1, column=0)
failed_button.config(
    border=0,
    highlightthickness=0,
)

img_check_button = PhotoImage(file=r"Day - 31\Day 31 - Project\right.png")

check_button = Button(
    image=img_check_button,
    command=lambda: (change_word(), remove_words_from_list(None)),
)
check_button.grid(row=1, column=1)
check_button.config(border=0, highlightthickness=0)


if __name__ == "__main__":
    root.mainloop()
