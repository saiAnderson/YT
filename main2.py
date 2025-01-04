import yt_dlp
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def select_save_path():
    """讓使用者選擇下載儲存目錄"""
    directory = filedialog.askdirectory()
    if directory:
        save_path.set(directory)
        path_label.config(text=f"儲存目錄：{directory}")

def update_progress(progress_text, value=0):
    """更新進度條與進度標籤"""
    progress_label.config(text=progress_text)
    progress_bar["value"] = value
    root.update_idletasks()

def clear_input():
    """清空 URL 輸入框"""
    url_entry.delete(0, tk.END)

def download_audio():
    """下載音樂的主要邏輯"""
    url = url_entry.get().strip()
    directory = save_path.get()

    if not url:
        messagebox.showerror("錯誤", "請輸入有效的 YouTube URL")
        return

    if not directory:
        messagebox.showerror("錯誤", "請選擇儲存目錄")
        return

    update_progress("正在準備下載...", 0)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(directory, "temp_audio.%(ext)s"),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', 'audio')
            sanitized_title = "".join(c for c in title if c.isalnum() or c in " ._-")
            temp_audio_path = os.path.join(directory, "temp_audio.mp3")
            final_output_path = os.path.join(directory, f"{sanitized_title}.mp3")

            if os.path.exists(temp_audio_path):
                os.rename(temp_audio_path, final_output_path)
                update_progress("下載完成！", 100)
                messagebox.showinfo("完成", f"音樂已下載並儲存於：\n{final_output_path}")
                clear_input()  # 成功後清空輸入框
            else:
                messagebox.showerror("錯誤", "下載失敗，暫存檔案不存在")
    except Exception as e:
        update_progress("下載失敗", 0)
        messagebox.showerror("錯誤", f"下載過程中出現問題：\n{e}")

# 主視窗
root = tk.Tk()
root.title("YouTube 音樂下載器")
root.geometry("600x400")

# 標題區
header_frame = tk.Frame(root, bg="lightblue", height=50)
header_frame.pack(fill=tk.X)
header_label = tk.Label(header_frame, text="YouTube 音樂下載器", bg="lightblue", font=("Arial", 16, "bold"))
header_label.pack(pady=10)

# 內容區
content_frame = tk.Frame(root)
content_frame.pack(pady=20)

# URL 輸入框
tk.Label(content_frame, text="YouTube 音樂 URL：", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
url_entry = tk.Entry(content_frame, width=50, font=("Arial", 12))
url_entry.grid(row=0, column=1, padx=10, pady=10)

# 儲存路徑選擇
save_path = tk.StringVar()
tk.Button(content_frame, text="選擇儲存目錄", command=select_save_path, font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10)
path_label = tk.Label(content_frame, text="儲存目錄：未選擇", font=("Arial", 10))
path_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# 下載按鈕
download_button = tk.Button(content_frame, text="下載音樂", command=download_audio, font=("Arial", 12), bg="lightblue")
download_button.grid(row=2, columnspan=2, pady=20)

# 進度條
progress_label = tk.Label(root, text="", font=("Arial", 10))
progress_label.pack()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# 啟動主迴圈
root.mainloop()
