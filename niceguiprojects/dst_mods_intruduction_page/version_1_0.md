### 功能设计
Excel 文件解析更新进数据库
- pandas
- excel 文件同步/异步解析
- update_or_insert

图片存储
- excel 中单元格的图片进行本地文件系统存储
- 数据库字段只存储固定路径，这意味着后续只需要更新对应路径的图片内容即可，数据库不必更新
- 关于图片解析并更新，图片是否存在时间戳等关键信息，对比后再更新？

文件上传
- 上传 excel 文件
- 异步更新数据库

文件下载
- 下载最新 excel 文件

### 技术总览
- excel parse
- async parse
- database and async database
- file upload and download
- nicegui
- sqlalchemy
- pandas
- ...
