# 独立使用 Django ORM

## 注意事项

---

必须在导入 django 内容前设置 DJANGO_SETTINGS_MODULE：

`os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoorm.djangoorm.settings")`

所以，djangoorm 的使用，似乎应该只从 `__init__.py` 处引入比较好？或者引入一个 load_djangoorm 函数？

---

INSTALLED_APPS 中包含的 apps 的相对路径是从项目启动（python main.py）的位置开始的！！！

---