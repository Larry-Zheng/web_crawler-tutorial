from selenium import  webdriver
import time
import re
import csv
from urllib import request
import requests
from PIL import Image

if __name__ == '__main__':
    #新建csv文件
    csvF = open('qqFriens.csv','w',newline='')
    csvW = csv.writer(csvF)


    #访问主页面
    url = 'https://mail.qq.com/'
    opt = webdriver.ChromeOptions()
    # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
    opt.set_headless()
    driver=webdriver.Chrome(options=opt)
    driver.maximize_window()
    driver.get(url)

    #切换frame 输入账号密码 登录
    driver.switch_to.frame('login_frame')
    driver.find_element_by_id('switcher_plogin').click()  #找账号登陆字样 并点击
    a=driver.find_element_by_id('u')
    a.clear()
    a.send_keys('519334736')
    b=driver.find_element_by_id('p')
    b.clear()
    b.send_keys('*') #see another py for hint
    driver.find_element_by_id('login_button').click()
    driver.implicitly_wait(5)
    # time.sleep(2)

    #点击通信录
    driver.find_element_by_xpath('//*[@id="navBarTd"]/li[3]/a').click()
    # time.sleep(1)
    driver.implicitly_wait(5)


    #抓取好友 detail跳转点击处
    driver.switch_to.frame('mainFrame')
    friends = driver.find_elements_by_xpath('//*[@id="list"]/ul/div/li/span[1]')
    driver.implicitly_wait(5)


    # friends[1].click()
    # time.sleep(2)
    # driver.find_element_by_css_selector('#bar > div > div > a.btn_gray.btn_space.btn_back.left').click()
    # time.sleep(2)
    # js = 'window.open("%s");'%driver.current_url
    # driver.execute_script(js)
    # time.sleep(2)

    for f in friends[1:]:
        f.click()
        driver.implicitly_wait(5)

        mail  = driver.find_element_by_xpath('//*[@id="info"]/div/div/dl/dd/a[1]').text
        try :
            qq = re.search(r'(.*)@qq',mail).group(1)
            nickName = driver.find_element_by_xpath('//*[@id="info"]/div/div/h3').text
            picUrl = driver.find_element_by_xpath('//*[@id="info"]/div/div/img').get_attribute('src')

            # cookieList = driver.get_cookies()
            # keyDict = {}
            # for cL in cookieList:
            #     k = cL.get('name')
            #     v = cL.get('value')
            #     keyDict[k] = v

            print((qq, nickName, picUrl))

            #写入图片

            mainHandle = driver.current_window_handle  #主句柄
            driver.execute_script('window.open("%s")'%picUrl)
            driver.switch_to.window(driver.window_handles[-1])  #js执行后会有一个新句柄 切换到那个窗口
            # print(driver.find_element_by_xpath('/html/body/img'))
            # ActionChains(driver).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()

            #截图
            driver.save_screenshot(r".\heads\screenshot.png")  #先存截屏图片
            # imgElement  = driver.find_element_by_xpath('/html/body/img')
            # location = imgElement.location  #定位图片位置
            # size = imgElement.size  #定位图片大小
            coderange = (380,280,419,319)  # 写成我们需要截取的位置坐标

            I = Image.open(r".\heads\screenshot.png")
            # print(coderange)
            headImg = I.crop(coderange)
            headImg.save(r'.\heads\%s.png'%qq)

            driver.close()  #关闭当前标签页
            driver.switch_to.window(mainHandle)  #返回主句柄
            csvW.writerow((qq,nickName))


        except Exception as e:
            print(e)
            continue


        finally:
            try:
                driver.switch_to.frame('mainFrame')
            except :
                pass
            driver.find_element_by_css_selector('#bar > div > div > a.btn_gray.btn_space.btn_back.left')\
                .click()  #返回
            driver.implicitly_wait(10)
            time.sleep(0.5)


    csvF.close()
    driver.close()