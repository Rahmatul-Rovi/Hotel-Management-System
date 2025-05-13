import customtkinter as ctk
from tkinter import messagebox

# Set appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Main App
class HotelApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🏨 Hotel Management System")
        self.geometry("1100x700")
        self.resizable(False, False)

        self.bookings = []  # Store all bookings

        # Header
        header = ctk.CTkLabel(self, text="HOTEL MANAGEMENT SYSTEM", font=("Arial", 28, "bold"))
        header.pack(pady=20)

        # Content Frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.build_form()

    def build_form(self):
        # --- LEFT FORM AREA ---
        form_frame = ctk.CTkFrame(self.content_frame, width=400)
        form_frame.pack(side="left", padx=30, pady=20)

        ctk.CTkLabel(form_frame, text="Customer Name:", font=("Arial", 16)).pack(anchor="w", pady=(10, 0))
        self.name_entry = ctk.CTkEntry(form_frame, width=250)
        self.name_entry.pack()

        ctk.CTkLabel(form_frame, text="Phone Number:", font=("Arial", 16)).pack(anchor="w", pady=(10, 0))
        self.phone_entry = ctk.CTkEntry(form_frame, width=250)
        self.phone_entry.pack()

        ctk.CTkLabel(form_frame, text="Room Type:", font=("Arial", 16)).pack(anchor="w", pady=(10, 0))
        self.room_type = ctk.CTkComboBox(form_frame, values=["Single", "Double", "Deluxe", "Suite"], width=250)
        self.room_type.set("Single")
        self.room_type.pack()

        ctk.CTkLabel(form_frame, text="Stay Duration (days):", font=("Arial", 16)).pack(anchor="w", pady=(10, 0))
        self.days_entry = ctk.CTkEntry(form_frame, width=250)
        self.days_entry.pack()

        # --- BUTTON AREA ---
        button_frame = ctk.CTkFrame(form_frame)
        button_frame.pack(pady=20)

        ctk.CTkButton(button_frame, text="Book Room", command=self.book_room, width=120).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Delete Booking", command=self.delete_booking, width=120).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Clear Form", command=self.clear_form, width=120).grid(row=1, column=0, padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Reset System", command=self.reset_system, width=120).grid(row=1, column=1, padx=5, pady=5)

        # --- RIGHT DISPLAY AREA ---
        self.right_frame = ctk.CTkFrame(self.content_frame)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=30, pady=20)

        self.status_label = ctk.CTkLabel(self.right_frame, text="Welcome to our Hotel!", font=("Arial", 18))
        self.status_label.pack(pady=10)

        ctk.CTkLabel(self.right_frame, text="📋 Bookings Summary", font=("Arial", 16)).pack(pady=(10, 5))

        self.booking_listbox = ctk.CTkTextbox(self.right_frame, width=550, height=400, font=("Courier", 14))
        self.booking_listbox.pack()

    def book_room(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        room = self.room_type.get()
        days = self.days_entry.get().strip()

        if not name or not phone or not days:
            messagebox.showwarning("Missing Data", "Please fill out all fields.")
            return

        try:
            days = int(days)
        except ValueError:
            messagebox.showerror("Invalid Input", "Stay Duration must be a number.")
            return

        booking_info = f"{name} | {phone} | {room} | {days} days"
        self.bookings.append(booking_info)

        self.status_label.configure(text=f"✅ Room booked for {name} ({room} - {days} days)")
        self.update_booking_list()
        self.clear_form()

    def delete_booking(self):
        selected_text = self.booking_listbox.get("insert linestart", "insert lineend")
        if selected_text.strip() in self.bookings:
            self.bookings.remove(selected_text.strip())
            self.status_label.configure(text="❌ Booking deleted successfully.")
            self.update_booking_list()
        else:
            messagebox.showerror("Not Found", "No booking selected or booking not found.")

    def clear_form(self):
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.days_entry.delete(0, "end")
        self.room_type.set("Single")
        self.status_label.configure(text="🧹 Form cleared.")

    def reset_system(self):
        self.bookings.clear()
        self.update_booking_list()
        self.clear_form()
        self.status_label.configure(text="🔄 System reset.")

    def update_booking_list(self):
        self.booking_listbox.delete("0.0", "end")
        if not self.bookings:
            self.booking_listbox.insert("end", "No bookings yet.\n")
        else:
            for i, booking in enumerate(self.bookings, start=1):
                self.booking_listbox.insert("end", f"{i}. {booking}\n")


if __name__ == "__main__":
    app = HotelApp()
    app.mainloop()
