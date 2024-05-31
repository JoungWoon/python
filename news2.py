import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import webbrowser

# Function to fetch and display titles from the website
def display_titles():
    url = 'https://www.ppomppu.co.kr/zboard/zboard.php?id=freeboard'
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for title_tag in soup.find_all('a', class_='baseList-title'):
            if not title_tag.find_parent('tr', class_='baseNotice'):
                title = title_tag.get_text().strip()
                board_num_tag = title_tag.find_parent('tr', class_='baseList')
                board_num_tags = board_num_tag.find('td', class_='baseList-numb')
                board_num = board_num_tags.get_text().strip() if board_num_tags else ""
                additional_text_tag = title_tag.find_next_sibling('span', class_='baseList-c')
                comment = additional_text_tag.get_text().strip() if additional_text_tag else "0"
                if title:
                    # Check for duplicates
                    existing_items = {tree.item(item, "values")[0]: item for item in tree.get_children()}
                    if board_num in existing_items:
                        # Update existing item
                        tree.item(existing_items[board_num], values=(board_num, title, comment))
                    else:
                        # Add new item
                        tree.insert("", "end", values=(board_num, title, comment))
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

# Function to display the content of the selected title
def show_url_content(event):
    selected_item = tree.selection()[0]
    no = tree.item(selected_item, "values")[0]
    url = f"https://m.ppomppu.co.kr/new/bbs_view.php?id=freeboard&no={no}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        content_tag = soup.find('div', class_='cont')
        content = content_tag.get_text() if content_tag else "<p>No content found</p>"
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, content)
    except requests.RequestException as e:
        print(f"Error fetching content: {e}")

# Initialize main window
root = tk.Tk()
root.title("뽐뿌 News")
root.geometry("1024x800")

# Fetch button at the top
fetch_button = tk.Button(root, text="게시물 가져오기", command=display_titles)
fetch_button.pack(pady=10)

# Left frame for Treeview and Text box
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Right frame for Treeview's Scrollbar
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Treeview widget
tree = ttk.Treeview(left_frame, columns=("no", "title", "comment"), show='headings')
tree.column("no", width=100, minwidth=100)
tree.column("title", width=500, minwidth=500)
tree.column("comment", width=100, minwidth=100)
tree.heading("no", text="번호", anchor=tk.W)
tree.heading("title", text="타이틀", anchor=tk.W)
tree.heading("comment", text="댓글수", anchor=tk.W)

# Scrollbar for Treeview
scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side="left", fill="both", expand=True)

# Text box for displaying content
text_box = tk.Text(left_frame)
text_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Bind event for Treeview selection
tree.bind("<<TreeviewSelect>>", show_url_content)

# Initial display of titles
display_titles()

# Start the main event loop
root.mainloop()
