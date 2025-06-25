import tkinter as tk
from tkinter import ttk, scrolledtext
# import openai  # 需要安装 openai 库: pip install openai

# 替换为你的 OpenAI API 密钥
# openai.api_key = "your_api_key_here"

class AIChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("轻量级 AI 对话程序")
        self.root.geometry("600x500")
        self.root.minsize(400, 300)  # 添加最小尺寸限制
        self.root.resizable(True, True)

        # 上下文记忆设置
        self.context_memory = 5  # 默认 5 句记忆
        self.conversation_history = []

        # 创建界面
        self._create_widgets()

        # 模拟历史对话（实际使用时删除）
        self.conversation_history = [
            {"role": "assistant", "content": "你好！我是AI助手，有什么可以帮您的？"}
        ]
        self.update_chat_display()

    def _create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 上下文记忆选择
        context_frame = ttk.LabelFrame(main_frame, text="上下文记忆设置", padding=10)
        context_frame.pack(fill=tk.X, pady=(0, 10))

        self.memory_var = tk.IntVar(value=5)
        ttk.Radiobutton(context_frame, text="5 句记忆", variable=self.memory_var,
                        value=5, command=self.update_memory_setting).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(context_frame, text="10 句记忆", variable=self.memory_var,
                        value=10, command=self.update_memory_setting).pack(side=tk.LEFT, padx=10)

        # 聊天记录显示
        chat_frame = ttk.LabelFrame(main_frame, text="对话记录", padding=10)
        chat_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 10)
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.tag_config("user", foreground="blue")
        self.chat_display.tag_config("assistant", foreground="green")

        # 用户输入区域 - 修复布局问题
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 使用 grid 布局管理器确保输入框和按钮正确显示
        self.user_input = ttk.Entry(input_frame)
        self.user_input.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        send_button = ttk.Button(input_frame, text="发送", command=self.send_message)
        send_button.grid(row=0, column=1)
        
        # 配置列权重，使输入框可以扩展
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, minsize=80)  # 按钮最小宽度

        # 绑定回车键事件
        self.user_input.bind("<Return>", self.send_message)
        
        # 设置焦点到输入框
        self.user_input.focus_set()

    def update_memory_setting(self):
        """更新上下文记忆设置"""
        self.context_memory = self.memory_var.get()
        self.trim_conversation_history()

    def trim_conversation_history(self):
        """修剪对话历史，保留最近的指定数量对话"""
        # 保留最近的 n 条消息（系统消息始终保留）
        max_messages = self.context_memory
        if len(self.conversation_history) > max_messages:
            # 始终保留第一条系统消息
            system_msg = self.conversation_history[0]
            recent_msgs = self.conversation_history[-max_messages + 1:]
            self.conversation_history = [system_msg] + recent_msgs

    def update_chat_display(self):
        """更新聊天显示区域"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)

        for msg in self.conversation_history:
            role = msg["role"]
            content = msg["content"]

            if role == "user":
                self.chat_display.insert(tk.END, "你: ", "user")
            elif role == "assistant":
                self.chat_display.insert(tk.END, "AI: ", "assistant")

            self.chat_display.insert(tk.END, f"{content}\n\n")

        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)  # 滚动到底部

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
        
        # 设置焦点回输入框
        self.user_input.focus_set()

    def get_ai_response(self):
        """获取AI回复（模拟或真实API调用）"""
        # 在实际应用中，取消注释以下代码并替换为你的API密钥
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            return f"发生错误: {str(e)}"
        """

        # 模拟回复（实际使用时删除这部分）
        last_user_msg = self.conversation_history[-1]["content"]
        memory_size = self.context_memory

        # 根据记忆大小生成不同的回复
        if memory_size == 5:
            return f"（5句记忆模式）我收到了你的消息：'{last_user_msg}'。\n当前记忆容量：5条消息。"
        else:
            return f"（10句记忆模式）我理解了：'{last_user_msg}'。\n当前可以记住更多上下文（10条消息）。"


if __name__ == "__main__":
    root = tk.Tk()
    app = AIChatApp(root)
    root.mainloop()
