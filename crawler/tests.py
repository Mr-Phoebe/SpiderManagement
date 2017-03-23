import codecs


def print_temp(fa, flag):
    f1 = codecs.open('testha.txt', 'a+', encoding='utf-8')
    f1.write(str(fa))
    s = flag * 10
    f1.write(s + "\n")
    f1.close()


def print_temp_line(line, num, dep):
    f1 = codecs.open('test' + str(num) + '_' + str(dep) + '.txt', 'a+', encoding='utf-8')
    for i in line:
        f1.write(str(i) + "\n")
    f1.write("\n**************\n")
    f1.close()


def test(soup_packetpage):
    dic_test = {"class": ["brand-info", "brand-value-change", "brand-col-8"]}

    li = soup_packetpage.findAll("div", dic_test)
    for item in li:
        if 'class' in item.attrs \
                and item.attrs['class'] == ["brand-info", "brand-value-change", "brand-col-8"]:
            print(item)
