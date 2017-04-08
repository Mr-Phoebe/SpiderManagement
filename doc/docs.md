名词定义
---

抓取网址：由用户输入的需要抓取的网址

抓取内容：由用户输入的需要抓取的内容

![]()

HTML语法树：HTML结构是一棵严格的多叉树，拥有唯一根节点

节点：在HTML中为某一个具体的标签

叶子节点：在HTML中为某一个具体的字符串

路径：从根节点`<html>`到某个节点经过的各个节点

锚：每个顺序包含抓取内容中每一个字符的叶子节点





对象定义
---

contend：抓取内容，str对象

url：抓取网址，str对象

BeautifulSoup：HTML语法树，由BeautifulSoup对HTML源码进行结构化分析而得到的BeautifulSoup对象

Node：节点，对BeautifulSoup中T的ag对象进行了封装后得到

Leaves：叶子节点，为BeautifulSoup中的NavigableString对象

anchor：包含所有锚的list对象


