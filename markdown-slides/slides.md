% Markdown+Beamer+Pandoc幻灯片模板
% 吴章金 @ 泰晓科技 | TinyLab.org
% \today

# 准备环境

## 安装pandoc

- 以Ubuntu为例

    sudo apt-get install pandoc

- 其他平台

    请参考[pandoc首页](http://johnmacfarlane.net/pandoc/installing.html)

## 安装Latex以及中文支持

- 以Ubuntu为例

```
    $ sudo apt-get install texlive-xetex \
        texlive-latex-recommended \
        texlive-latex-extra \
        latex-cjk-common latex-cjk-chinese \
        latex-cjk-chinese-arphic-bkai00mp \
        latex-cjk-chinese-arphic-bsmi00lp \
        latex-cjk-chinese-arphic-gbsn00lp \
        latex-cjk-chinese-arphic-gkai00mp \
```

## 安装Beamer

- 以Ubuntu为例

```
    sudo apt-get install latex-beamer
```

- 相关用法与实例

```
    $ ls /usr/share/doc/latex-beamer/
    beameruserguide.pdf.gz
    examples
    solutions
```

## 安装字体

```
    $ sudo apt-get install \
        fonts-arphic-bkai00mp \
        fonts-arphic-bsmi00lp \
        fonts-arphic-gbsn00lp \
        fonts-arphic-gkai00mp \
        ttf-wqy-microhei \
        ttf-wqy-zenhei
```

## 配置字体

- 列出可选字体

```
    $ fc-list | egrep "wqy|AR"
```

- 实例配置：需配置zh_template.tex如下：

```
    \setCJKmainfont{AR PL KaitiM GB} % 中文字体
```

# 编写幻灯

## 幻灯首页

-   前三行分别对应
    -   标题
    -   作者
    -   日期

- 例如：

```
    % Markdown+Beamer+Pandoc幻灯片模板
    % 吴章金 @ 泰晓科技 | TinyLab.org
    % \today
```

## 幻灯正文

-   支持如下语法
    - [Markdown基本语法](http://wowubuntu.com/markdown/)
    - [Pandoc Markdown语法](http://johnmacfarlane.net/pandoc/demo/example9/pandocs-markdown.html)
    - Latex语法：[1](http://www.maths.tcd.ie/~dwilkins/LaTeXPrimer/),[2](http://latex-project.org/guides/)

-   实例

```
    # In the morning

    ## Getting up

    - Turn off alarm
    - Get out of bed
```

# 格式转换

## 生成pdf

- 利用该模板

```
    $ make pdf & make read
```

- 原生命令

```
    pandoc -t beamer --toc \
        -V theme:Darmstadt \
        -V fontsize:9pt \
        slides.md -o slides.pdf \
        --latex-engine=xelatex \
        --template=./templates/zh_template.tex
```

## 生成html

- 利用该模板

```
   $ make html & make read-html
```

- 原始命令

```
    pandoc -t dzslides -s --mathjax \
        slides.md -o slides.html
```

# 参考资料

------------------

- [Write Beamer or Html slide using Markdown and Pandoc](https://github.com/herrkaefer/herrkaefer.github.io/blob/master/_posts/2013-12-17-write-beamer-or-html-slide-using-markown-and-pandoc.markdown)
- [Producing slide shows with pandoc](http://johnmacfarlane.net/pandoc/README.html#producing-slide-shows-with-pandoc)

# 致谢

------------------

\centerline{\includegraphics[height=3in]{images/thanks.jpg}}
<p align="center"><img src="images/thanks.jpg" height="90%" /></p>
