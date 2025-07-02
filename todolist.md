探索 ipython、jupter notebook

---

探索 django-extensions

---

juptyer notebook + python manager.py shell
```bash
python ./backend/manage.py shell --notebook
```
为什么没有上面的命令？

---

为什么 Django Server 无法使用？
```txt
PermissionError: [Errno 13] Permission denied: 'D:\\Software\\JetBrains\\PyCharm 2024.1.4\\jbr\\bin'
```
我创建了新项目，只下载 django 库，没问题。

我同样创建了新项目，将代码复制过去（排除了 .idea、.venv），下载依赖库，有问题。

故，我猜测是第三方库的原因。

---

如何解决下面的内容：
```txt
WARNING:
This is a development server. Do not use it in a production setting.
Use a production WSGI or ASGI server instead.
```
即如何使用 WSGI 或 ASGI 服务器？

---

```txt
.venv\Lib\site-packages\coreapi\utils.py:5: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
```

---

确定一下，drf 能否做到 django-ninja/fastapi 那样详尽的自动生成的接口文档？

---

研究 django 的 values 前后的区别，效果不一样。有个效果是 group by，另一个忘了。

---

