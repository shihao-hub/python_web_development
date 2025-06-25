import tkinter as tk
from tkinter import ttk, scrolledtext


def send_message(self, event=None):
    """发送用户消息并获取AI回复"""
    user_text = self.user_input.get().strip()
    if not user_text:
        return

    # 添加用户消息到历史
    self.conversation_history.append({"role": "user", "content": user_text})
    self.user_input.delete(0, tk.END)
    self.update_chat_display()

    # 获取AI回复（模拟或真实API调用）
    ai_response = self.get_ai_response()

    # 添加AI回复到历史
    self.conversation_history.append({"role": "assistant", "content": ai_response})
    self.trim_conversation_history()
    self.update_chat_display()

root = tk.Tk()
root.title("轻量级 AI 对话程序")
root.geometry("600x500")
root.resizable(True, True)

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill=tk.BOTH, expand=True)

input_frame = ttk.Frame(main_frame, padding=(0, 10, 0, 0))
input_frame.pack(fill=tk.X)

user_input = ttk.Entry(input_frame)
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
user_input.bind("<Return>", send_message)

send_button = ttk.Button(input_frame, text="发送", command=send_message)
send_button.pack(side=tk.RIGHT)

root.mainloop()
