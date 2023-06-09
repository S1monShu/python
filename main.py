from flask import Flask, jsonify, request, render_template
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from flaskext.mysql import MySQL
import time
from threading import *

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'Guitar'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parser', methods=["POST"])

def parser():
    def parserAllCpu():
        def parserCpuPaginate():
                hrefMyztorg = [0]
                arrHref = []
                arrTitleGuitar = []
                
                for i in range(7, 8):
                    driver = webdriver.Chrome()
                    href = f"https://skifmusic.ru/catalog/bas-gitaryi-14/page{i}"
                    driver.get(href)

                    allCpu = driver.find_elements(By.CLASS_NAME, "js-product-link")
                    print(len(allCpu))

                    countCpu = (len(allCpu))

                    for number in range(countCpu):
                        arrHref += ([allCpu[number].get_attribute("href")])
                        arrTitleGuitar += ([allCpu[number].text])

            
                    for number in range(len(arrHref) - countCpu, len(arrHref)):
                
                        driver.get(arrHref[number+number])
                        name = driver.find_element(By.CLASS_NAME, "header-h1").text
                        if name.find("'") != -1:
                            guitarName = name.rpartition("'")[0]
                        else:
                            guitarName = name.rpartition("'")[2]
                        guitarPrice = driver.find_element(By.CLASS_NAME, "bigger-170").text
                        if len(driver.find_elements(By.XPATH, "//li[@data-index='2']/img")) > 0:
                            guitarImgTwo = driver.find_element(By.XPATH, "//li[@data-index='2']/img").get_attribute("src")
                        else:
                            guitarImgTwo = 'Нету второй фотографии'
                        if len(driver.find_elements(By.XPATH, "//li[@data-index='3']/img")) > 0:
                            guitarImgThree = driver.find_element(By.XPATH, "//li[@data-index='3']/img").get_attribute("src")
                        else:
                            guitarImgThree = 'Нету третьей фотографии'
                        guitarImg = driver.find_element(By.CLASS_NAME, "product-images-gallery__item").get_attribute("data-src")
                        if len(driver.find_elements(By.CLASS_NAME, "list-unstyled")) > 0:
                            guitarDescription = driver.find_elements(By.CLASS_NAME, "list-unstyled")
                        else:
                            print('1')

                        obj = Guitar(guitarName, guitarPrice, guitarImg, guitarImgTwo, guitarImgThree, guitarDescription[0].text, arrHref[number+number])
                        print(obj.name)
                        print(obj.price)
                        print(obj.img)
                        print(obj.imgTwo)
                        print(obj.imgThree)
                        print(obj.description)
                        print(obj.skifHref)
                        href = "https://www.muztorg.ru/"
                        driver.get(href)
                        time.sleep(2.5)
                        driver.find_element(By.CLASS_NAME, "form-control").send_keys(obj.name)
                        driver.find_element(By.CLASS_NAME, "header__search-button").click()
                        time.sleep(1)
                        if len(driver.find_elements(By.CLASS_NAME, "product-thumbnail")) > 0:
                            print('Есть совпадение')
                            myzHref = driver.find_element(By.XPATH, "//div[@class='title']/a").get_attribute("href")
                            hrefMyztorg[0] = myzHref
                        else:
                            print('Нету на сайте')
                            hrefMyztorg[0] = 'Нету'
                            print(hrefMyztorg[0])

                        print(hrefMyztorg[0])
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute(f"INSERT INTO `Bass_guitars` (`name`, `price`, `img`, `imgTwo`, `imgThree` ,`specifications`, `skifHref`, `myzHref`) VALUES ('{obj.name}', '{obj.price}', '{obj.img}', '{obj.imgTwo}', '{obj.imgThree}' , '{obj.description}', '{obj.skifHref}', '{hrefMyztorg[0]}')")
                        conn.commit()
                driver.close()
   


                 
                 
                 

             

        class Guitar:
            def __init__(self, name, price, img, imgTwo, imgThree, description, skifHref):
                self.name = name
                self.price = price
                self.img = img
                self.imgTwo = imgTwo
                self.imgThree = imgThree
                self.description = description
                self.skifHref = skifHref

 
        

        parserCpuPaginate()
        
                

        return "end"
    

    parserAllCpu()
   
    return render_template('end.html')
    


if __name__ == "__main__":
    app.run(debug=True)
