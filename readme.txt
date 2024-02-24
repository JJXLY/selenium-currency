从中国银行外汇牌价网站：https://www.boc.cn/sourcedb/whpj/  爬取数据。
仅需运行 main.py 即可。
爬取英文代码和中文名称，但发现两个网站有许多不一致的地方，因此在 currency_trans.txt 中手动整理了标准符号和货币名称的对应关系。
爬到的数据保存于 result.txt 中
例如，在终端运行：
python main.py 20211231 USD
输出：636.99
