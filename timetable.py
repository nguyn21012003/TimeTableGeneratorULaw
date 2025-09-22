import os
import sys

import customtkinter as ctk
import pandas as pd

ctk.set_appearance_mode("Light")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


theme_path = resource_path("themes/cherry.json")
ctk.set_default_color_theme(theme_path)


import customtkinter as ctk
import pandas as pd


class App(ctk.CTk):
    def __init__(self, height, width):
        super().__init__()
        self.title("Time Table Generator only for ULAW")
        self.geometry(f"{width}x{height}")
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.font20 = ("Montserrat", 20)

        # header / controls
        self.numSubjectsLabel = ctk.CTkLabel(self, text="Số lượng môn:", font=self.font20)
        self.numSubjectsLabel.grid(row=0, column=0, padx=20, pady=10)

        self.numSubjectsEntry = ctk.CTkEntry(self, placeholder_text="vd: 3", font=self.font20)
        self.numSubjectsEntry.grid(row=0, column=1, padx=20, pady=10)

        self.createFieldsButton = ctk.CTkButton(self, text="Tạo", command=self.createFields, font=self.font20)
        self.createFieldsButton.grid(row=0, column=2, padx=20, pady=10)

        self.cosoLabel = ctk.CTkLabel(self, text="Cơ sở:", font=self.font20)
        self.cosoLabel.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.placeVar = ctk.StringVar(value="1")
        self.place1 = ctk.CTkRadioButton(self, text="Cơ sở 1", variable=self.placeVar, value="1", font=self.font20)
        self.place1.grid(row=1, column=1, padx=5, pady=5)
        self.place2 = ctk.CTkRadioButton(self, text="Cơ sở 2", variable=self.placeVar, value="2", font=self.font20)
        self.place2.grid(row=1, column=2, padx=5, pady=5)
        self.place3 = ctk.CTkRadioButton(self, text="Cơ sở 3", variable=self.placeVar, value="3", font=self.font20)
        self.place3.grid(row=1, column=3, padx=5, pady=5)

        self.rows_frame = ctk.CTkFrame(self)
        self.rows_frame.grid(row=3, column=0, columnspan=6, sticky="nsew", padx=10, pady=5)

        self.subjectRows = []

        for i in range(6):
            self.grid_columnconfigure(i, weight=1)

    def createFields(self):
        for widget in self.rows_frame.winfo_children():
            widget.destroy()
        if hasattr(self, "generateButton") and self.generateButton is not None:
            try:
                self.generateButton.destroy()
            except:
                pass
        if hasattr(self, "displayBox") and self.displayBox is not None:
            try:
                self.displayBox.destroy()
            except:
                pass

        self.subjectRows.clear()

        try:
            num = int(self.numSubjectsEntry.get())
        except:
            return

        dayOptions = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]

        for i in range(num):
            subjectLabel = ctk.CTkLabel(self.rows_frame, text=f"Môn học {i+1}", font=self.font20)
            subjectLabel.grid(row=i, column=0, padx=10, pady=5, sticky="ew")

            subjectEntry = ctk.CTkEntry(self.rows_frame, placeholder_text="Tên môn", font=self.font20)
            subjectEntry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

            periodEntry = ctk.CTkEntry(self.rows_frame, placeholder_text="Tiết học", font=self.font20)
            periodEntry.grid(row=i, column=2, padx=10, pady=5, sticky="ew")

            weekEntry = ctk.CTkEntry(self.rows_frame, placeholder_text="Tuần học", font=self.font20)
            weekEntry.grid(row=i, column=3, padx=10, pady=5, sticky="ew")

            roomEntry = ctk.CTkEntry(self.rows_frame, placeholder_text="Phòng học", font=self.font20)
            roomEntry.grid(row=i, column=4, padx=10, pady=5, sticky="ew")

            dayDropdown = ctk.CTkOptionMenu(self.rows_frame, values=dayOptions, font=self.font20)
            dayDropdown.grid(row=i, column=5, padx=10, pady=5, sticky="ew")

            self.subjectRows.append([subjectEntry, periodEntry, weekEntry, roomEntry, dayDropdown])

        self.generateButton = ctk.CTkButton(self, text="Tạo thời khoá biểu", command=self.generateResults, font=self.font20)
        self.generateButton.grid(row=4, column=0, columnspan=6, pady=20)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

        self.displayBox = ctk.CTkTextbox(self, width=500, height=400, font=self.font20)
        self.displayBox.grid(row=5, column=0, columnspan=6, padx=20, pady=10)

    def generateResults(self):
        self.displayBox.delete("0.0", "end")
        data = []
        place = self.placeVar.get()
        for idx, row in enumerate(self.subjectRows):
            subjectValue = str(row[0].get().strip() or "Chưa nhập môn học")
            periodValue = str(row[1].get().strip() or "Chưa nhập tiết học")
            weekValue = str(row[2].get().strip() or "Chưa nhập tuần học")
            roomValue = str(row[3].get().strip() or "Chưa nhập phòng học")
            dayValue = row[4].get()

            schedule = get_schedule(int(place), periodValue)
            if schedule:
                start_time, end_time = schedule[0][0], schedule[-1][1]
                timeInfo = f"{start_time} → {end_time}"
            else:
                timeInfo = "Không rõ giờ"

            self.displayBox.insert("end", f"Cơ sở: {place}\n")
            self.displayBox.insert("end", f"Môn {idx+1}: {subjectValue}\n")
            self.displayBox.insert("end", f"Ngày: {dayValue}\n")
            self.displayBox.insert("end", f"Tiết: {timeInfo}\n")
            self.displayBox.insert("end", f"Tuần: {weekValue}\n")
            self.displayBox.insert("end", f"Phòng: {roomValue}\n\n")

            data.append([place, subjectValue, dayValue, timeInfo, weekValue, roomValue])

        df = pd.DataFrame(data, columns=["Cơ sở", "Môn học", "Ngày học", "Tiết học", "Tuần học", "Phòng học"])
        df.to_excel("TimeTable.xlsx", index=False)
        self.displayBox.insert("end", "✅ Kết quả đã lưu vào TimeTable.xlsx\n")


def get_schedule(coso: int, buoi: str):
    schedule = {}
    lenPeriod = len(buoi)

    if lenPeriod == 5 and coso in (1, 2):
        if buoi == "12345":  # sáng
            return [("07:00", "07:50"), ("07:50", "08:40"), ("08:40", "09:30"), ("09:45", "10:35"), ("10:35", "11:25")]
        elif buoi == "78901":  # chiều
            return [("13:00", "13:50"), ("13:50", "14:40"), ("14:40", "15:30"), ("15:45", "16:35"), ("16:35", "17:25")]
        elif buoi == "23456":  # tối
            return [("18:00", "18:50"), ("18:50", "19:40"), ("19:40", "20:30"), ("20:40", "21:30"), ("21:30", "22:20")]

    if lenPeriod == 4 and coso in (1, 2):
        if buoi == "12345":  # sáng
            return [("07:00", "07:50"), ("07:50", "08:40"), ("08:55", "09:45"), ("09:45", "10:35")]
        elif buoi == "78901":  # chiều
            return [("13:00", "13:50"), ("13:50", "14:40"), ("14:55", "15:45"), ("15:45", "16:35")]
        elif buoi == "23456":  # tối
            return [("18:00", "18:50"), ("18:50", "19:40"), ("19:55", "20:45"), ("20:45", "21:35")]

    if lenPeriod == 4 and coso == 3:
        if buoi == "12345":  # sáng
            return [("07:30", "08:20"), ("08:20", "09:10"), ("09:25", "10:15"), ("10:15", "11:05")]
        elif buoi == "78901":  # chiều
            return [("12:25", "13:15"), ("13:15", "14:05"), ("14:20", "15:10"), ("15:10", "16:00")]
        elif buoi == "23456":  # tối
            return [("18:00", "18:50"), ("18:50", "19:40"), ("19:55", "20:45"), ("20:45", "21:35")]

    return schedule


if __name__ == "__main__":

    app = App(900, 950)
    # Runs the app
    app.mainloop()
