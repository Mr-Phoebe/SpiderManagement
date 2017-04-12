名词定义
---

抓取网址：由用户输入的需要抓取的网址

抓取内容：由用户输入的需要抓取的内容

```
<html>
    <head>
        <title>
            My title
        </title>
    </head>
    <body>
        <a href="">
            My link
        </a>
        <h1>
            My header
        </h1>
        <div>
            <p>This is the first block. </p>
            <p>This is the second block. </p>
            <p>This is the third block. </p>
        </div>
    </body>
</html>
```

![](https://github.com/Mr-Phoebe/SpiderManagement/blob/master/doc/%E8%AF%AD%E6%B3%95%E6%A0%91.png)

Dom树：HTML结构是一棵严格的多叉树，拥有唯一根节点`<html>`

节点：在HTML中为某一个具体的标签，如`<head>`

叶子节点：在HTML中为某一个具体的字符串，如`My title`

路径：从根节点到某个节点经过的各个节点，如“This is the first block”的路径为，$P_1 = $`{<html>, <body>, <div>, <p>, This is the first block}`

锚：顺序包含抓取内容各个字符的叶子节点，可能有多个

路径相似度：用评估函数预估出两个路径的相似度，取值为[0, 1]

列表类网页：在网页中存在大量相似结构的少量文本模块，节点数多，但是叶子结点的字符串长度较小

新闻类网页：在网页中存在一块多量文本模块与多块是少量文本模块，节点数较少，但是部分叶子节点的字符串长度大

对象定义
---

contend：抓取内容，str对象，长度上限为128

url：抓取网址，str对象

BeautifulSoup：Dom树，由BeautifulSoup对HTML源码进行结构化分析而得到的BeautifulSoup对象

Node：节点，对BeautifulSoup中T的ag对象进行了封装后得到

Leaves：叶子节点，为BeautifulSoup中的NavigableString对象

anchor：包含所有锚的list对象


锚定位算法
---

### 功能

选取出所有的锚

### 返回

None

### 过程描述

用深度优先搜索搜索整个Dom树，并通过孩子的个数找出每一个叶子节点
判断叶子结点的字符串是否顺序包含抓取内容的每个字符，若是，则将此叶子节点加入anchor列表

### 伪代码

```
get_anchor_pos(Node):
    if Node.children == 0: # 没有孩子节点，则是叶子节点
        if substringcmp(Node.string, contend): # 查看是否满足顺序包含子串字符的条件
            将Node加入anchor
    else:
        for child in Node.children:
            get_anchor_pos(child)
```


### 复杂度分析

N : Dom树的节点的总个数
n : 叶子节点个数，且n<N
m : 最长叶子节点字符串的长度

#### 时间复杂度

搜索节点的时间复杂度为O(N)。  

单次比较字符的最坏时间复杂度为O(m)，有相关剪枝操作，时间复杂度与抓取内容的长度无关。  

总的时间复杂度为O(N+n*m)=O(n*m)

介于新闻类网页的m常常会较大，此算法在列表类网页表现较为迅速，不善于处理新闻类网页。

#### 空间复杂度

此算法的空间复杂度为O(N+n)