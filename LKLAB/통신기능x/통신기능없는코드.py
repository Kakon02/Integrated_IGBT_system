import os
import sys
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, PhotoImage

current_path = os.path.dirname(os.path.abspath(__file__))
loop_status_list = []
operation_value = False
timeline = 0


def center_window(window, window_width, window_height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    screen_center_x = (screen_width / 2) - (window_width / 2)
    screen_center_y = (screen_height / 2) - (window_height / 2)
    window.geometry(f"{window_width}x{window_height}+{int(screen_center_x)}+{int(screen_center_y)}")


def set_image(filename):
    folder_path = os.path.join(current_path, "image")
    image_path = os.path.join(folder_path, filename)
    image = Image.open(image_path)
    image_file = ImageTk.PhotoImage(image)
    return image_file


def is_temp_number(new_value):
    if new_value == "":
        return True
    elif new_value == "-":
        return True
    try:
        float(new_value)
        return True
    except ValueError:
        return False


def is_time_number(new_value):
    if new_value == "":
        return True
    try:
        int(new_value)
        return True
    except ValueError:
        return False


def exit_main_window():
    main_window.destroy()
    sys.exit()


def reset_loop_setting():
    loop_setting_temp_main_window_text.delete(0, tk.END)
    loop_setting_hour_main_window_text.delete(0, tk.END)
    loop_setting_min_main_window_text.delete(0, tk.END)
    loop_setting_sec_main_window_text.delete(0, tk.END)


def add_loop_setting():
    global loop_status_list
    loop_temp_value = loop_setting_temp_main_window_text.get()
    if loop_temp_value == "" or loop_temp_value == "-":
        loop_temp_value = "0"
    loop_hour_value = loop_setting_hour_main_window_text.get()
    if loop_hour_value == "":
        loop_hour_value = "0"
    loop_min_value = loop_setting_min_main_window_text.get()
    if loop_min_value == "":
        loop_min_value = "0"
    loop_sec_value = loop_setting_sec_main_window_text.get()
    if loop_sec_value == "":
        loop_sec_value = "0"
    if len(loop_status_list) < 32:
        loop_status_list.append(loop_temp_value)
        loop_status_list.append(loop_hour_value)
        loop_status_list.append(loop_min_value)
        loop_status_list.append(loop_sec_value)


def loop_status_insert():
    global loop_status_list
    loop_status_text_list = [num_1_temp_loop_status_main_window_text, num_1_hour_loop_status_main_window_text,
                             num_1_min_loop_status_main_window_text, num_1_sec_loop_status_main_window_text,
                             num_2_temp_loop_status_main_window_text, num_2_hour_loop_status_main_window_text,
                             num_2_min_loop_status_main_window_text, num_2_sec_loop_status_main_window_text,
                             num_3_temp_loop_status_main_window_text, num_3_hour_loop_status_main_window_text,
                             num_3_min_loop_status_main_window_text, num_3_sec_loop_status_main_window_text,
                             num_4_temp_loop_status_main_window_text, num_4_hour_loop_status_main_window_text,
                             num_4_min_loop_status_main_window_text, num_4_sec_loop_status_main_window_text,
                             num_5_temp_loop_status_main_window_text, num_5_hour_loop_status_main_window_text,
                             num_5_min_loop_status_main_window_text, num_5_sec_loop_status_main_window_text,
                             num_6_temp_loop_status_main_window_text, num_6_hour_loop_status_main_window_text,
                             num_6_min_loop_status_main_window_text, num_6_sec_loop_status_main_window_text,
                             num_7_temp_loop_status_main_window_text, num_7_hour_loop_status_main_window_text,
                             num_7_min_loop_status_main_window_text, num_7_sec_loop_status_main_window_text,
                             num_8_temp_loop_status_main_window_text, num_8_hour_loop_status_main_window_text,
                             num_8_min_loop_status_main_window_text, num_8_sec_loop_status_main_window_text]
    for num in range(len(loop_status_text_list)):
        text_list = loop_status_text_list[num]
        text_list.config(state="normal")
        text_list.delete(0, tk.END)
        text_list.config(state="disabled")
    for num in range(len(loop_status_list)):
        text_list = loop_status_text_list[num]
        loop_data = loop_status_list[num]
        text_list.config(state="normal")
        text_list.insert(0, loop_data)
        text_list.config(state="disabled")

    main_window.after(50, loop_status_insert)


def del_1st_loop():
    global loop_status_list
    for i in range(4):
        try:
            loop_status_list.pop(0)
        except IndexError:
            pass


def del_2nd_loop():
    global loop_status_list
    for i in range(4):
        try:
            loop_status_list.pop(4)
        except IndexError:
            pass


def del_3rd_loop():
    global loop_status_list
    for i in range(4):
        try:
            loop_status_list.pop(8)
        except IndexError:
            pass


def del_4th_loop():
    global loop_status_list
    for i in range(4):
        try:
            loop_status_list.pop(12)
        except IndexError:
            pass


def del_5th_loop():
    global loop_status_list
    for i in range(4):
        try:
            loop_status_list.pop(16)
        except IndexError:
            pass


def del_6th_loop():
    global loop_status_list
    for i in range(4):
        try:
            loop_status_list.pop(20)
        except IndexError:
            pass


def del_7th_loop():
    global loop_status_list
    for i in range(4):
        try:
            loop_status_list.pop(24)
        except IndexError:
            pass


def del_8th_loop():
    global loop_status_list
    for i in range(4):
        try:
            loop_status_list.pop(28)
        except IndexError:
            pass


def run_stop_background():
    global operation_value
    if operation_value is True:
        run_stop_main_window_button.config(text="Stop", bg="red", fg="black", font=("Arial", 25, "bold"))
    else:
        run_stop_main_window_button.config(text="Run", bg="blue", fg="white", font=("Arial", 25, "bold"))
    main_window.after(50, run_stop_background)


def serial_running():
    global operation_value, timeline
    if operation_value is True:
        operation_value = False

    else:
        timeline = 0
        operation_value = True
        timeline = 0


def run_time_status():
    global operation_value, timeline
    if operation_value is True:
        timeline += 1
    timeline_hour = timeline//3600
    timeline_min = (timeline-timeline_hour*3600)//60
    timeline_sec = timeline % 60
    run_time_main_window_text.config(state='normal')
    run_time_main_window_text.delete(0, tk.END)
    run_time_main_window_text.insert(0, f'{timeline_hour}시간{timeline_min}분{timeline_sec}초')
    run_time_main_window_text.config(state='disabled')
    main_window.after(1000, run_time_status)


def serial_cur_npv_nsv():

    main_window.after(50, serial_cur_npv_nsv)


def serial_change_nsv():
    pass


def checking_input_num():
    change_set_temp_value = change_set_temp_main_window_text.get()
    loop_setting_temp_value = loop_setting_temp_main_window_text.get()
    loop_setting_hour_value = loop_setting_hour_main_window_text.get()
    loop_setting_min_value = loop_setting_min_main_window_text.get()
    loop_setting_sec_value = loop_setting_sec_main_window_text.get()
    if change_set_temp_value == "" or change_set_temp_value == "-":
        change_set_temp_value = '0'
    change_set_temp_value = float(change_set_temp_value)
    if change_set_temp_value < -20:
        change_set_temp_main_window_text.delete(0, tk.END)
        change_set_temp_main_window_text.insert(0, "-20")
    elif change_set_temp_value > 150:
        change_set_temp_main_window_text.delete(0, tk.END)
        change_set_temp_main_window_text.insert(0, "150")
    if loop_setting_temp_value == "" or loop_setting_temp_value == "-":
        loop_setting_temp_value = '0'
    loop_setting_temp_value = float(loop_setting_temp_value)
    if loop_setting_temp_value < -20:
        loop_setting_temp_main_window_text.delete(0, tk.END)
        loop_setting_temp_main_window_text.insert(0, "-20")
    elif loop_setting_temp_value > 150:
        loop_setting_temp_main_window_text.delete(0, tk.END)
        loop_setting_temp_main_window_text.insert(0, "150")
    if loop_setting_hour_value == "":
        loop_setting_hour_value = '0'
    loop_setting_hour_value = int(loop_setting_hour_value)
    if loop_setting_hour_value > 99:
        loop_setting_hour_main_window_text.delete(0, tk.END)
        loop_setting_hour_main_window_text.insert(0, "99")
    if loop_setting_min_value == "":
        loop_setting_min_value = '0'
    loop_setting_min_value = int(loop_setting_min_value)
    if loop_setting_min_value > 59:
        loop_setting_min_main_window_text.delete(0, tk.END)
        loop_setting_min_main_window_text.insert(0, "59")
    if loop_setting_sec_value == "":
        loop_setting_sec_value = '0'
    loop_setting_sec_value = int(loop_setting_sec_value)
    if loop_setting_sec_value > 59:
        loop_setting_sec_main_window_text.delete(0, tk.END)
        loop_setting_sec_main_window_text.insert(0, "59")
    main_window.after(50, checking_input_num)


def serial_set_temp_p1():
    pass


def serial_set_temp_pd1():
    pass


def serial_set_temp_m1():
    pass


def serial_set_temp_md1():
    pass


def serial_run_loop():
    global current_path, loop_status_list
    folder_path = os.path.join(current_path, "txt")
    txt_path = os.path.join(folder_path, "loop.txt")
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write(f"{loop_status_list}")


def load_loop():
    global current_path, loop_status_list
    folder_path = os.path.join(current_path, "txt")
    txt_path = os.path.join(folder_path, "loop.txt")
    with open(txt_path, 'r', encoding='utf-8') as file:
        content = file.read()
    loop_status_list = []
    content_list = content.strip('[]').replace("'", "").split(',')
    for item in content_list:
        if item.strip():
            num = float(item.strip())
            if num.is_integer():
                loop_status_list.append(int(num))
            else:
                loop_status_list.append(num)


main_window = tk.Tk()
center_window(main_window, 1000, 800)
main_window.resizable(width=False, height=False)
main_window_background = tk.Canvas(main_window, width=1000, height=800)
main_window_background.pack(fill="both", expand=False)
canvas_background = set_image("background.png")
if canvas_background is not None:
    main_window_background.create_image(0, 0, image=canvas_background, anchor="nw")
    main_window_background.photo = canvas_background
temp_validate = (main_window.register(is_temp_number), '%P')
time_validate = (main_window.register(is_time_number), '%P')
exit_main_window_button = tk.Button(main_window, text="Exit", font=("Arial", 30, 'bold'), fg="white",
                                    bg='red', command=exit_main_window)
exit_main_window_button.place(x=852, y=151, width=147, height=49)
loop_setting_temp_main_window_text = tk.Entry(main_window, font=("Arial", 36, 'bold'), fg="black",
                                              validate='key', validatecommand=temp_validate)
loop_setting_temp_main_window_text.place(x=20, y=375, width=200, height=70)
loop_setting_hour_main_window_text = tk.Entry(main_window, font=("Arial", 36, 'bold'), fg="black",
                                              validate='key', validatecommand=time_validate)
loop_setting_hour_main_window_text.place(x=120, y=465, width=100, height=70)
loop_setting_min_main_window_text = tk.Entry(main_window, font=("Arial", 36, 'bold'), fg="black",
                                             validate='key', validatecommand=time_validate)
loop_setting_min_main_window_text.place(x=120, y=555, width=100, height=70)
loop_setting_sec_main_window_text = tk.Entry(main_window, font=("Arial", 36, 'bold'), fg="black",
                                             validate='key', validatecommand=time_validate)
loop_setting_sec_main_window_text.place(x=120, y=645, width=100, height=70)
reset_loop_setting_main_window_button = tk.Button(main_window, text="Reset", font=("Arial", 28, "bold"),
                                                  bg="white", command=reset_loop_setting)
reset_loop_setting_main_window_button.place(x=20, y=740, width=120, height=50)
num_1_temp_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_1_temp_loop_status_main_window_text.place(x=400, y=375, width=100, height=40)
num_1_temp_loop_status_main_window_text.config(state="disabled")
num_2_temp_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_2_temp_loop_status_main_window_text.place(x=400, y=425, width=100, height=40)
num_2_temp_loop_status_main_window_text.config(state="disabled")
num_3_temp_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_3_temp_loop_status_main_window_text.place(x=400, y=475, width=100, height=40)
num_3_temp_loop_status_main_window_text.config(state="disabled")
num_4_temp_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_4_temp_loop_status_main_window_text.place(x=400, y=525, width=100, height=40)
num_4_temp_loop_status_main_window_text.config(state="disabled")
num_5_temp_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_5_temp_loop_status_main_window_text.place(x=400, y=575, width=100, height=40)
num_5_temp_loop_status_main_window_text.config(state="disabled")
num_6_temp_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_6_temp_loop_status_main_window_text.place(x=400, y=625, width=100, height=40)
num_6_temp_loop_status_main_window_text.config(state="disabled")
num_7_temp_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_7_temp_loop_status_main_window_text.place(x=400, y=675, width=100, height=40)
num_7_temp_loop_status_main_window_text.config(state="disabled")
num_8_temp_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_8_temp_loop_status_main_window_text.place(x=400, y=725, width=100, height=40)
num_8_temp_loop_status_main_window_text.config(state="disabled")
num_1_hour_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_1_hour_loop_status_main_window_text.place(x=550, y=375, width=50, height=40)
num_1_hour_loop_status_main_window_text.config(state="disabled")
num_2_hour_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_2_hour_loop_status_main_window_text.place(x=550, y=425, width=50, height=40)
num_2_hour_loop_status_main_window_text.config(state="disabled")
num_3_hour_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_3_hour_loop_status_main_window_text.place(x=550, y=475, width=50, height=40)
num_3_hour_loop_status_main_window_text.config(state="disabled")
num_4_hour_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_4_hour_loop_status_main_window_text.place(x=550, y=525, width=50, height=40)
num_4_hour_loop_status_main_window_text.config(state="disabled")
num_5_hour_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_5_hour_loop_status_main_window_text.place(x=550, y=575, width=50, height=40)
num_5_hour_loop_status_main_window_text.config(state="disabled")
num_6_hour_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_6_hour_loop_status_main_window_text.place(x=550, y=625, width=50, height=40)
num_6_hour_loop_status_main_window_text.config(state="disabled")
num_7_hour_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_7_hour_loop_status_main_window_text.place(x=550, y=675, width=50, height=40)
num_7_hour_loop_status_main_window_text.config(state="disabled")
num_8_hour_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_8_hour_loop_status_main_window_text.place(x=550, y=725, width=50, height=40)
num_8_hour_loop_status_main_window_text.config(state="disabled")
num_1_min_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_1_min_loop_status_main_window_text.place(x=650, y=375, width=50, height=40)
num_1_min_loop_status_main_window_text.config(state="disabled")
num_2_min_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_2_min_loop_status_main_window_text.place(x=650, y=425, width=50, height=40)
num_2_min_loop_status_main_window_text.config(state="disabled")
num_3_min_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_3_min_loop_status_main_window_text.place(x=650, y=475, width=50, height=40)
num_3_min_loop_status_main_window_text.config(state="disabled")
num_4_min_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_4_min_loop_status_main_window_text.place(x=650, y=525, width=50, height=40)
num_4_min_loop_status_main_window_text.config(state="disabled")
num_5_min_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_5_min_loop_status_main_window_text.place(x=650, y=575, width=50, height=40)
num_5_min_loop_status_main_window_text.config(state="disabled")
num_6_min_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_6_min_loop_status_main_window_text.place(x=650, y=625, width=50, height=40)
num_6_min_loop_status_main_window_text.config(state="disabled")
num_7_min_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_7_min_loop_status_main_window_text.place(x=650, y=675, width=50, height=40)
num_7_min_loop_status_main_window_text.config(state="disabled")
num_8_min_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_8_min_loop_status_main_window_text.place(x=650, y=725, width=50, height=40)
num_8_min_loop_status_main_window_text.config(state="disabled")
num_1_sec_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_1_sec_loop_status_main_window_text.place(x=750, y=375, width=50, height=40)
num_1_sec_loop_status_main_window_text.config(state="disabled")
num_2_sec_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_2_sec_loop_status_main_window_text.place(x=750, y=425, width=50, height=40)
num_2_sec_loop_status_main_window_text.config(state="disabled")
num_3_sec_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_3_sec_loop_status_main_window_text.place(x=750, y=475, width=50, height=40)
num_3_sec_loop_status_main_window_text.config(state="disabled")
num_4_sec_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_4_sec_loop_status_main_window_text.place(x=750, y=525, width=50, height=40)
num_4_sec_loop_status_main_window_text.config(state="disabled")
num_5_sec_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_5_sec_loop_status_main_window_text.place(x=750, y=575, width=50, height=40)
num_5_sec_loop_status_main_window_text.config(state="disabled")
num_6_sec_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_6_sec_loop_status_main_window_text.place(x=750, y=625, width=50, height=40)
num_6_sec_loop_status_main_window_text.config(state="disabled")
num_7_sec_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_7_sec_loop_status_main_window_text.place(x=750, y=675, width=50, height=40)
num_7_sec_loop_status_main_window_text.config(state="disabled")
num_8_sec_loop_status_main_window_text = tk.Entry(main_window, font=("Arial", 20, "bold"))
num_8_sec_loop_status_main_window_text.place(x=750, y=725, width=50, height=40)
num_8_sec_loop_status_main_window_text.config(state="disabled")
add_loop_setting_main_window_button = tk.Button(main_window, text="Add", font=("Arial", 28, "bold"),
                                                bg="white", command=add_loop_setting)
add_loop_setting_main_window_button.place(x=160, y=740, width=120, height=50)
num_1_delete_loop_status_main_window_button = tk.Button(main_window, text="X", font=("Arial", 25),
                                                        bg="white", command=del_1st_loop)
num_1_delete_loop_status_main_window_button.place(x=820, y=375, width=40, height=40)
num_2_delete_loop_status_main_window_button = tk.Button(main_window, text="X", font=("Arial", 25),
                                                        bg="white", command=del_2nd_loop)
num_2_delete_loop_status_main_window_button.place(x=820, y=425, width=40, height=40)
num_3_delete_loop_status_main_window_button = tk.Button(main_window, text="X", font=("Arial", 25),
                                                        bg="white", command=del_3rd_loop)
num_3_delete_loop_status_main_window_button.place(x=820, y=475, width=40, height=40)
num_4_delete_loop_status_main_window_button = tk.Button(main_window, text="X", font=("Arial", 25),
                                                        bg="white", command=del_4th_loop)
num_4_delete_loop_status_main_window_button.place(x=820, y=525, width=40, height=40)
num_5_delete_loop_status_main_window_button = tk.Button(main_window, text="X", font=("Arial", 25),
                                                        bg="white", command=del_5th_loop)
num_5_delete_loop_status_main_window_button.place(x=820, y=575, width=40, height=40)
num_6_delete_loop_status_main_window_button = tk.Button(main_window, text="X", font=("Arial", 25),
                                                        bg="white", command=del_6th_loop)
num_6_delete_loop_status_main_window_button.place(x=820, y=625, width=40, height=40)
num_7_delete_loop_status_main_window_button = tk.Button(main_window, text="X", font=("Arial", 25),
                                                        bg="white", command=del_7th_loop)
num_7_delete_loop_status_main_window_button.place(x=820, y=675, width=40, height=40)
num_8_delete_loop_status_main_window_button = tk.Button(main_window, text="X", font=("Arial", 25),
                                                        bg="white", command=del_8th_loop)
num_8_delete_loop_status_main_window_button.place(x=820, y=725, width=40, height=40)
run_stop_main_window_button = tk.Button(main_window, command=serial_running)
run_stop_main_window_button.place(x=85, y=65, width=80, height=80)
run_time_main_window_text = tk.Entry(main_window, font=("Arial", 22, "bold"))
run_time_main_window_text.place(x=260, y=75, width=230, height=60)
run_time_main_window_text.config(state="disabled")
cur_temp_main_window_text = tk.Entry(main_window, width=6, font=("Arial", 36, 'bold'), fg="black")
cur_temp_main_window_text.place(x=20, y=220)
cur_temp_main_window_text.config(state="disabled")
set_temp_main_window_text = tk.Entry(main_window, width=6, font=("Arial", 36, 'bold'), fg="black")
set_temp_main_window_text.place(x=270, y=220)
set_temp_main_window_text.config(state="disabled")
change_set_temp_main_window_text = tk.Entry(main_window, font=("Arial", 36, 'bold'), fg="black",
                                            validate='key', validatecommand=temp_validate)
change_set_temp_main_window_text.place(x=530, y=130, width=180, height=70)
apply_change_set_temp_main_window_button = tk.Button(main_window, text="SET", font=("Arial", 20, 'bold'), fg="black",
                                                     bg="white", command=serial_change_nsv)
apply_change_set_temp_main_window_button.place(x=770, y=130, width=70, height=70)
instant_change_set_p1_temp_main_window_button = tk.Button(main_window, text="+1", font=("Arial", 20, 'bold'),
                                                          fg="black", bg="white", command=serial_set_temp_p1)
instant_change_set_p1_temp_main_window_button.place(x=510, y=213, width=75, height=75)
instant_change_set_pd1_temp_main_window_button = tk.Button(main_window, text="+0.1", font=("Arial", 20, 'bold'),
                                                           fg="black", bg="white", command=serial_set_temp_pd1)
instant_change_set_pd1_temp_main_window_button.place(x=595, y=213, width=75, height=75)
instant_change_set_m1_temp_main_window_button = tk.Button(main_window, text="-1", font=("Arial", 20, 'bold'),
                                                          fg="black", bg="white", command=serial_set_temp_m1)
instant_change_set_m1_temp_main_window_button.place(x=680, y=213, width=75, height=75)
instant_change_set_md1_temp_main_window_button = tk.Button(main_window, text="-0.1", font=("Arial", 20, 'bold'),
                                                           fg="black", bg="white", command=serial_set_temp_md1)
instant_change_set_md1_temp_main_window_button.place(x=765, y=213, width=75, height=75)
load_loop_status_main_window_button = tk.Button(main_window, text="Load Loop", font=("Arial", 25, "bold"),
                                                bg="white", command=load_loop)
load_loop_status_main_window_button.place(x=320, y=320, width=180, height=50)
run_loop_status_main_window_button = tk.Button(main_window, text="Run Loop", font=("Arial", 25, "bold"),
                                               bg="white", command=serial_run_loop)
run_loop_status_main_window_button.place(x=800, y=320, width=180, height=50)
loop_status_insert()
run_stop_background()
run_time_status()
serial_cur_npv_nsv()
checking_input_num()
main_window.mainloop()
