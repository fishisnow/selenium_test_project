自动化脚本写入字符叠加

思路：
从csv文件中读取url和其对应的字符叠加，存入字典中，循环写入
环境：
1. python环境 2.7
2. 安装selenium包: pip install selenium
3. selenium3版本需要安装浏览器驱动
   http://docs.seleniumhq.org/download/中下载对应浏览器的驱动（火狐是GeckoDriver）
   并将驱动路径配置到windows环境变量中
4. 配置自动化脚本执行的浏览器环境（自动加载需要的流媒体插件）

文档：
1. Dos执行：python pydoc -m -p 1234
浏览器访问selenium对应文档
2. 参照《selenium2 python自动化测试实战》

后续改进：
1. 加入其他摄像机的逻辑
2. 完善异常处理
3. 加入多线程处理