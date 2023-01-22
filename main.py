import copy
import json
from tkinter import *
from tkinter import ttk
import tkinter as tk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, total_width, total_height, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        # Here set size of canvas per requirements TODO set args in class instantiation
        # canvas = tk.Canvas(self)
        canvas = tk.Canvas(self, width=total_width, height=total_height, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        # canvas.pack(side="left", fill="both", expand=True)
        # scrollbar.pack(side="right", fill="y")
        canvas.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky=N + S + W)


class MyFirstGUI:
    def __init__(self, master, filename):
        self.master = master
        self.master.title("Flexible Preferences GUI")

        # Initialize style
        s = ttk.Style()
        # Create style used by default for all Frames
        # s.configure('TFrame', background='yellow')

        # Create style for the first frame
        s.configure('Frame1.TFrame', background='red')
        # Create separate style for the second frame
        s.configure('Frame2.TFrame', background='green')

        self.total_width = 500
        self.total_height = 300

        self.frame_left = ttk.Frame(self.master, style='Frame1.TFrame')
        self.frame_left.grid(column=0, row=0, sticky=N)

        self.create_scrollable_frame()

        self.frame_bottom = ttk.Frame(self.master)
        self.frame_bottom.grid(column=0, columnspan=2, row=1)

        self.create_buttons()

        self.current_category_selection = None
        self.category_current_row = 0
        self.category_buttons = []
        self.options_current_row = 0
        self.options_fields = []
        self.options_fields_values = []

        self.working_config = json.load(open(filename))
        print(self.working_config)
        self.reference_config = copy.deepcopy(self.working_config)

        self.initiate_settings_from_file()

    def create_scrollable_frame(self):
        self.frame_right_sc = ScrollableFrame(self.master, style='Frame2.TFrame',
                                              total_width=self.total_width,
                                              total_height=self.total_height)
        self.frame_right_sc.grid(column=1, row=0, sticky=N)

    def create_buttons(self):
        self.ok_button = Button(self.frame_bottom, text='OK', command=self.clicked_ok_button)
        self.ok_button.grid(column=0, row=0, padx=5, pady=10)

        self.cancel_button = Button(self.frame_bottom, text='Cancel', command=self.close_window)
        self.cancel_button.grid(column=1, row=0, padx=5, pady=10)

    def initiate_settings_from_file(self):
        for i, item in enumerate(self.working_config):
            if i == 0:
                first_item = item
            print(item)
            self.add_category(label=item)

        self.current_category_selection = first_item
        self.add_options(parent_label=first_item)

    def add_category(self, label):
        self.category_buttons.append(Button(
            self.frame_left,
            text=label,
            relief='flat',
            command=lambda c=len(self.category_buttons): self.change_tool(c)
        ))
        self.category_buttons[-1].grid(
            column=0,
            row=self.category_current_row,
            sticky=W + E)

        self.category_current_row += 1

        # self.close_button = Button(self.frame_left, text="Tool 2", relief='flat', command=self.change_tool)
        # self.close_button.grid(column=0, row=1)

        # self.close_button = Button(self.frame_left, text="Close", relief='flat', command=self.master.quit)
        # self.close_button.grid(column=0, row=5)

    def add_options(self, parent_label):
        print(f"parent label: {parent_label}")
        self.current_category_selection = parent_label
        for item in self.working_config[parent_label]:
            conf_name = item
            label = self.working_config[parent_label][item]['field_description']
            tag = self.working_config[parent_label][item]['type']
            current = self.working_config[parent_label][item]['current']

            ttk.Label(self.frame_right_sc.scrollable_frame,
                      text=label,
                      wraplength=self.total_width).grid(row=self.options_current_row,
                                                               column=0,
                                                               padx=5,
                                                               pady=5,
                                                               sticky=N + W)

            self.options_current_row += 1

            if tag == 'dropdown':
                options = self.working_config[parent_label][item]['options']
                self.add_options_dropdown(options_list=options, current_selection=current, name=conf_name)
            else:
                self.add_options_entry(current_text=current, name=conf_name)

            self.options_current_row += 1

    def add_options_dropdown(self, options_list, current_selection, name):
        self.options_fields_values.append(tk.StringVar())
        self.options_fields.append(ttk.Combobox(self.frame_right_sc.scrollable_frame,
                                                textvariable=self.options_fields_values[-1],
                                                width=15,
                                                state='readonly'))
        self.options_fields[-1]['values'] = tuple(options_list)
        self.options_fields[-1].current(current_selection)
        self.options_fields[-1].option_id = name
        self.options_fields[-1].grid(row=self.options_current_row,
                                     column=0,
                                     padx=5,
                                     pady=5,
                                     sticky=N + W)
        # ttk.Label(self.frame_right_sc.scrollable_frame,
        #           text='').grid(row=self.options_current_row + 1, column=0)

    def add_options_entry(self, current_text, name):
        self.options_fields_values.append(StringVar(self.master, value=current_text))
        self.options_fields.append(ttk.Entry(self.frame_right_sc.scrollable_frame,
                                             textvariable=self.options_fields_values[-1],
                                             width=30))
        self.options_fields[-1].option_id = name
        self.options_fields[-1].grid(row=self.options_current_row,
                                     column=0,
                                     padx=5,
                                     pady=5,
                                     sticky=N + W)

    def update_config_dict(self, node, value):
        self.working_config[self.current_category_selection][node]['current'] = value

    def update_working_config(self):
        for item in self.options_fields:
            current_id = item.option_id
            print(current_id)
            # print(type(item))
            if isinstance(item, tk.ttk.Combobox):
                # print(item['values'])
                current_selection = item.current()
                self.update_config_dict(node=current_id, value=current_selection)
            elif isinstance(item, tk.ttk.Entry):
                entry_value = item.get()
                self.update_config_dict(node=current_id, value=entry_value)
            else:
                print('not defined widget')

        print(self.reference_config)
        print(self.working_config)

    def close_window(self):
        self.master.quit()

    def clicked_ok_button(self):
        self.update_working_config()
        with open('../conf_out.json', 'w') as f:
            json.dump(self.working_config, f, indent=2)
        self.close_window()

        # ttk.Label(self.frame_right_sc.scrollable_frame,
        #           text='').grid(row=self.options_current_row + 1, column=0)

        # self.close_button = Button(self.frame_right_sc.scrollable_frame, text="Cat Option 1", relief='flat', command=self.master.quit)
        # self.close_button.grid(column=1, row=0, padx=5, pady=5, sticky=N+W)
        #
        # self.close_button2 = Button(self.frame_right_sc.scrollable_frame, text="Cat Option 2", relief='flat', command=self.master.quit)
        # self.close_button2.grid(column=1, row=1, padx=5, pady=5, sticky=N+W)
        #
        # self.n = tk.StringVar()
        # self.combo = ttk.Combobox(self.frame_right_sc.scrollable_frame,
        #                           width=15,
        #                           textvariable=self.n,
        #                           state='readonly')
        # self.combo['values'] = ('act 1', 'act 2', 'act 3')
        # self.combo.current(1)
        # self.combo.grid(row=2, column=1, padx=5, pady=5, sticky=N+W)
        #
        # self.entry = ttk.Entry(self.frame_right_sc.scrollable_frame, width=20)
        # self.entry.grid(row=3, column=1, padx=5, pady=5, sticky=N+W)

    def clear_widget(self, target_frame):
        for widget in target_frame.winfo_children():
            widget.destroy()

    def greet(self):
        print("Greetings! Clearing right frame")
        self.clear_widget(self.frame_right_sc)

    def change_tool(self, index):
        # Take current values and update temporary config dictionary
        self.update_working_config()

        print(index)
        btn_name = self.category_buttons[index].cget("text")
        print(btn_name)

        self.clear_widget(self.frame_right_sc)
        self.options_current_row = 0
        self.options_fields = []
        self.options_fields_values = []

        self.create_scrollable_frame()
        self.add_options(parent_label=btn_name)


root = Tk()

root.resizable(False, False)  # This code helps to disable windows from resizing

# window_height = 500
# window_width = 900
#
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
#
# x_cordinate = int((screen_width/4) - (window_width/2))
# y_cordinate = int((screen_height/2) - (window_height/2))
#
# root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

# root.columnconfigure(0, weight=1)
# root.columnconfigure(1, weight=3)
# root.columnconfigure(2, weight=2)

# Remove the Title bar of the window
# root.overrideredirect(True)

config_filename = 'conf.json'

my_gui = MyFirstGUI(root, config_filename)

root.unbind_all('<<NextWindow>>')  # Unbinding the behavior that causes Tab Cycling
root.mainloop()
