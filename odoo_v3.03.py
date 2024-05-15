import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, NoSuchWindowException
import time
import threading
import winsound

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Odoo Auto Reconciliation ")

        style = ttk.Style()
        style.theme_use('clam')

        self.label_user = ttk.Label(master, text="Username:")
        self.label_user.grid(row=0, column=0, padx=10, pady=5, sticky='e')

        self.entry_user = ttk.Entry(master,width=50)
        self.entry_user.grid(row=0, column=1, padx=20, pady=10)

        self.label_pass = ttk.Label(master, text="Password:")
        self.label_pass.grid(row=1, column=0, padx=10, pady=5, sticky='e')

        self.entry_pass = ttk.Entry(master, width=50, show="*")
        self.entry_pass.grid(row=1, column=1, padx=10, pady=5)

        self.label_max_clicks = ttk.Label(master, text="Max Clicks:")
        self.label_max_clicks.grid(row=2, column=0, padx=10, pady=5, sticky='e')

        self.entry_max_clicks = ttk.Entry(master, width=50)
        self.entry_max_clicks.insert(0, "80")  # Set default value to 80
        self.entry_max_clicks.grid(row=2, column=1, padx=10, pady=5)

        self.label_url = ttk.Label(master, text="URL:")
        self.label_url.grid(row=3, column=0, padx=10, pady=5, sticky='e')

        self.entry_url = ttk.Entry(master, width=50)
        self.entry_url.grid(row=3, column=1, padx=10, pady=5)

        self.button_login = ttk.Button(master, width=50, text="Login", command=self.start_thread)
        self.button_login.grid(row=4, columnspan=2, pady=10)

        self.log_text = scrolledtext.ScrolledText(master, height=10, width=50, wrap=tk.WORD)
        self.log_text.grid(row=5, columnspan=2, padx=10, pady=5, sticky='nsew')

        self.redirector = RedirectText(self.log_text)
        sys.stdout = self.redirector

        self.load_credentials()

        # Create the menu
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # Create the File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Create the About menu
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="Instructions", command=self.show_instructions)
        about_menu.add_command(label="About Us", command=self.show_about_us)  # Add About Us option
        menubar.add_cascade(label="About", menu=about_menu)

    def show_instructions(self):
        instructions_window = tk.Toplevel(self.master)
        instructions_window.title("Instructions")

        instructions_label = ttk.Label(instructions_window, text="بعد تسجل الدخول يسمح لك البرنامج ب 1 دقيقة قبل بدء التشغبل للتهيئة\n1.حدد الفواتير الغير مسدد\n2.رتب من الاقدم الى الاحدث\n3.حدد عدد الفواتير فى الصفحة الواحدة بالضغط على 80 الموجودة بالصفحة وعدلها لما تريد\n4.انتظر حتى انتها الدقيقة وبدء التشغيل.")
        instructions_label.pack(padx=10, pady=10)
    def show_about_us(self):
        about_us_window = tk.Toplevel(self.master)
        about_us_window.title("About Us")

        about_us_label = ttk.Label(about_us_window, text="We are a team dedicated to developing software solutions\n                     to streamline business processes.\n\n    Design by Evram wadeeh \n       +201007899697\n        acc.evram@gmail.com")
        about_us_label.pack(padx=10, pady=10)

    def start_thread(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        max_clicks = int(self.entry_max_clicks.get()) if self.entry_max_clicks.get() else None
        url = self.entry_url.get()
        self.save_credentials(username, password, url)
        threading.Thread(target=self.login, args=(username, password, max_clicks, url)).start()

    def login(self, username, password, max_clicks=None, url=None):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager().install()))

        try:
            if url:
                driver.get(url)

            username_input = driver.find_element(By.ID, 'login')
            password_input = driver.find_element(By.ID, 'password')
            username_input.send_keys(username)
            password_input.send_keys(password)

            submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_button.click()

            time.sleep(60)

            next_button_click_count = 0

            while True:
                retry_count = 0
                while retry_count < 3:
                    try:
                        buttons = driver.find_elements(By.XPATH, '//a[@data-id]')

                        if len(buttons) == 0:
                            name_element = driver.find_element(By.XPATH,
                                                               '//span[@class="o_field_char o_field_widget o_readonly_modifier o_required_modifier" and @name="name"]')
                            name_text = name_element.text
                            print("Name:", name_text)

                            next_button = driver.find_element(By.CLASS_NAME, 'o_pager_next')
                            next_button.click()
                            next_button_click_count += 1
                            print(f"'Next' button clicked {next_button_click_count} times.")
                            time.sleep(5)

                            if max_clicks is not None and next_button_click_count >= max_clicks:
                                print("Reached maximum number of clicks. Exiting.")
                                break
                            continue

                        data_ids = [int(button.get_attribute('data-id')) for button in buttons]
                        min_data_id = min(data_ids)

                        try:
                            min_button = driver.find_element(By.XPATH, f'//a[@data-id="{min_data_id}"]')
                            min_button.click()
                        except StaleElementReferenceException:
                            print("Stale element reference encountered. Refreshing and retrying...")
                            continue
                        except NoSuchElementException as e:
                            print("An element was not found:", e)
                            driver.quit()
                        except NoSuchWindowException as e:
                            print("No such window error occurred:", e)
                            driver.quit()

                        time.sleep(5)
                        break  # Break out of the retry loop if successful
                    except Exception as e:
                        print("An error occurred:", e)
                        retry_count += 1
                        print(f"Retrying ({retry_count}/3) after 10 seconds...")
                        winsound.Beep(1000, 200)  # Play beep sound
                        time.sleep(10)
                else:
                    print("Max retries reached. Exiting.")
                    break  # Break out of the main loop if max retries reached

        except NoSuchElementException as e:
            print("An element was not found:", e)
            messagebox.showerror("Error", "An element was not found.")
        except Exception as e:
            print("An error occurred:", e)
            messagebox.showerror("Error", "An error occurred.")
        finally:
            driver.quit()

    def load_credentials(self):
        try:
            with open("credentials.json", "r") as file:
                data = json.load(file)
                if "username" in data:
                    self.entry_user.insert(0, data["username"])
                if "password" in data:
                    self.entry_pass.insert(0, data["password"])
                if "url" in data:
                    self.entry_url.insert(0, data["url"])
        except FileNotFoundError:
            pass

    def save_credentials(self, username, password, url):
        data = {"username": username, "password": password, "url": url}
        with open("credentials.json", "w") as file:
            json.dump(data, file)


class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, str):
        self.text_widget.insert(tk.END, str)
        self.text_widget.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
