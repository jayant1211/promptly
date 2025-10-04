import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import calendar

class CTkDatePicker(ctk.CTkFrame):
    def __init__(self, master=None, font=("Segoe UI", 12), **kwargs):
        super().__init__(master, **kwargs)

        ctk.set_appearance_mode("Dark")
        self.configure(fg_color="#000000")  # pure black
        self.font = font

        # Entry
        self.date_entry = ctk.CTkEntry(
            self,
            fg_color="#000000",
            text_color="white",
            placeholder_text="Select Date",
            corner_radius=0,
            border_width=0,
            font=self.font
        )
        self.date_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Calendar button
        self.calendar_button = ctk.CTkButton(
            self,
            text="▼",
            width=25,
            fg_color="#000000",
            text_color="white",
            hover_color="#026fc9",
            border_width=0,
            corner_radius=0,
            font=self.font,
            command=self.open_calendar
        )
        self.calendar_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.popup = None
        self.selected_date = None
        self.date_format = "%m/%d/%Y"
        self.allow_manual_input = True
        self.allow_change_month = True
        self.add_months = 0
        self.subtract_months = 0

    def set_date_format(self, date_format):
        self.date_format = date_format

    def set_localization(self, localization):
        import locale
        locale.setlocale(locale.LC_ALL, localization)
        locale.setlocale(locale.LC_NUMERIC, "C")

    def open_calendar(self):
        if self.popup is not None:
            self.popup.destroy()
        self.popup = ctk.CTkToplevel(self)
        self.popup.title("Select Date")
        self.popup.configure(fg_color="#000000")
        self.popup.geometry("+%d+%d" % (self.winfo_rootx(), self.winfo_rooty() + self.winfo_height()))
        self.popup.resizable(False, False)
        self.popup.after(500, lambda: self.popup.focus())

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.build_calendar()

    def build_calendar(self):
        if hasattr(self, 'calendar_frame'):
            self.calendar_frame.destroy()

        self.calendar_frame = ctk.CTkFrame(self.popup, fg_color="#000000")
        self.calendar_frame.grid(row=0, column=0, padx=5, pady=5)

        # Adjust months
        for _ in range(self.add_months):
            if self.current_month == 12:
                self.current_month = 1
                self.current_year += 1
            else:
                self.current_month += 1
        for _ in range(self.subtract_months):
            if self.current_month == 1:
                self.current_month = 12
                self.current_year -= 1
            else:
                self.current_month -= 1

        # Month & Year label
        month_label = ctk.CTkLabel(
            self.calendar_frame,
            text=f"{calendar.month_name[self.current_month]}, {self.current_year}",
            font=self.font,
            text_color="white",
            fg_color="#000000"
        )
        month_label.grid(row=0, column=1, columnspan=5)

        if self.allow_change_month:
            prev_button = ctk.CTkButton(
                self.calendar_frame, text="<", width=25, fg_color="#000000",
                text_color="white", hover_color="#026fc9", border_width=0,
                corner_radius=0, font=self.font, command=self.prev_month
            )
            prev_button.grid(row=0, column=0)
            next_button = ctk.CTkButton(
                self.calendar_frame, text=">", width=25, fg_color="#000000",
                text_color="white", hover_color="#026fc9", border_width=0,
                corner_radius=0, font=self.font, command=self.next_month
            )
            next_button.grid(row=0, column=6)

        # Days header
        days = [calendar.day_name[i][:3] for i in range(7)]
        for i, day in enumerate(days):
            ctk.CTkLabel(self.calendar_frame, text=day, text_color="white",
                         fg_color="#000000", font=self.font).grid(row=1, column=i)

        # Days in month
        month_days = calendar.monthrange(self.current_year, self.current_month)[1]
        start_day = calendar.monthrange(self.current_year, self.current_month)[0]
        day = 1
        for week in range(2, 8):
            for day_col in range(7):
                if week == 2 and day_col < start_day or day > month_days:
                    ctk.CTkLabel(self.calendar_frame, text="", fg_color="#000000").grid(row=week, column=day_col)
                else:
                    btn = ctk.CTkButton(
                        self.calendar_frame, text=str(day), width=30,
                        fg_color="#000000", hover_color="#026fc9",
                        text_color="white", border_width=0, corner_radius=0,
                        font=self.font,
                        command=lambda d=day: self.select_date(d)
                    )
                    btn.grid(row=week, column=day_col, padx=2, pady=2)
                    day += 1

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.build_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.build_calendar()

    def select_date(self, day):
        self.selected_date = datetime(self.current_year, self.current_month, day)
        self.date_entry.configure(state='normal')
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, self.selected_date.strftime(self.date_format))
        if not self.allow_manual_input:
            self.date_entry.configure(state='disabled')
        if self.popup:
            self.popup.destroy()
            self.popup = None

    def get_date(self):
        return self.date_entry.get()

    def set_allow_manual_input(self, value):
        self.allow_manual_input = value
        self.date_entry.configure(state='normal' if value else 'disabled')

    def set_allow_change_month(self, value):
        self.allow_change_month = value

    def set_change_months(self, add_or_sub, value):
        if add_or_sub == "add":
            self.add_months = value
        elif add_or_sub == "sub":
            self.subtract_months = value
        else:
            raise ValueError("add_or_sub must be 'add' or 'sub'")
