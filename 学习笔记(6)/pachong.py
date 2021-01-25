
from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error
import xlwt
import sqlite3


def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getdata(baseurl)
    savepath = "豆瓣电影top250.xls"
    savedata(datalist,savepath)
findlink = re.compile(r'<a href="(.*?)">') #详情链接
findimgsrc = re.compile(r'<img.*src="(.*?)"',re.S) #图片
findtitle = re.compile(r'<span class="title">(.*)</span>') #片名
findrating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>') #评分
findjudge = re.compile(r'<span>(\d*)人评价</span>') #评价人数                           
findinq = re.compile(r'<span class="inq">(.*)</span>') #概况
findbd = re.compile(r'<p class="">(.*?)</p>',re.S) #相关内容


def getdata(baseurl):
    datalist = []
    for i in range(0,10):
        url = baseurl + str(i*25)
        html = askurl(url)
     
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            data = []
            item = str(item)

            link = re.findall(findlink,item)[0]
            data.append(link) #添加图片
            imgsrc = re.findall(findimgsrc,item)[0]
            data.append(imgsrc) #添加链接
            titles = re.findall(findtitle,item)
            if(len(titles) ==2):
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/","")
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')

            rating = re.findall(findrating,item)[0]
            data.append(rating)

            judgenum = re.findall(findjudge,item)[0]
            data.append(judgenum)

            inq = re.findall(findinq,item)
            if len(inq) != 0:
                inq = inq[0].replace("。","")
                data.append(inq)
            else:
                data.append(" ")

            bd = re.findall(findbd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)
            bd = re.sub('/'," ",bd)
            data.append(bd.strip())

            datalist.append(data)

            
    return datalist


def askurl(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75"
    }

    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

    return html


def savedata(datalist,savepath):
    
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet('豆瓣电影top250',cell_overwrite_ok=True)
    col = ("电影详情链接","图片链接","影片中文名","影片外文名","评分","评分数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    book.save(savepath)

if __name__ == "__main__":
    main()
    print("爬取完毕")
