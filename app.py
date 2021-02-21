from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import json
from datetime import datetime, timedelta
from time import sleep
from discord_webhook import DiscordWebhook,DiscordEmbed
from tokens import url_webhook
options = Options()
#Add Your CHROME USER PROFILE DIR HERE
options.add_argument("user-data-dir=")

def discord_zindabaad(status, classname, classtime, link, timeleft=0):
    webhook = DiscordWebhook(url=url_webhook)
    if timeleft != 0:
        timeleft = convert(timeleft)
    if status == 'waiting':
        embed = DiscordEmbed(title='Waiting For class', color=242424)
        embed.add_embed_field(name='Class', value=classname)
        embed.add_embed_field(name='Status', value=status)
        embed.add_embed_field(name='Time Left', value=timeleft)
        embed.add_embed_field(name='Class Time', value=classtime)
        embed.add_embed_field(name='Link', value=link)
    if status == 'Joined':
        embed = DiscordEmbed(title='Joined The Class', color=14177041)
        embed.add_embed_field(name='Class', value=classname)
        embed.add_embed_field(name='Status', value=status)
        embed.add_embed_field(name='Link', value=link)


    embed.set_footer(text="UTHH JA")
    webhook.add_embed(embed)
    webhook.execute()

    print("Sent message to discord")

def convert(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "%d:%02d:%02d" % (hour, min, sec)

def openClass(class_name, class_link):
    driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options=options)
    driver.get(class_link)
    sleep(5)
    #Mute This thing kept me waiting in iternal pain thanks to stackoverflow i can breath again ez but i am dumb
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('d').key_up(Keys.CONTROL).perform()
    #Camera Mute
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('e').key_up(Keys.CONTROL).perform()
    print(f'''Ready to Join Class {class_name}, Joining .....''')
    driver.find_element_by_xpath("/html/body/div[1]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]").click()
    discord_zindabaad('Joined', class_name, 0,class_link, 0)
    sleep(60)
    driver.close()

def get_schedule(day):
    f = open("classSchedule.json")
    y = json.load(f)
    y = y.get('Mon')
    return y

def timeleft(classtime):
    now = datetime.now()
    l = list(map(int, classtime.split(":")))
    secsleft = int((timedelta(hours=24) - (now - now.replace(hour=l[0], minute=l[1], second=0, microsecond=0))).total_seconds() % (24 * 3600))
    return secsleft


def class_schedule():
    t = datetime.now()
    t_day = t.strftime("%a")
    y = get_schedule(t_day)
    for class_time in y:
        #Refreashing Schedule but i dont kno if this is correct way to do that
        y = get_schedule(t_day)
        time = datetime.now().strftime("%H:%M")
        if time == class_time:
            openClass(y[class_time][0], y[class_time][1])
        elif time != class_time:
            sec_left = timeleft(class_time)
            # print("Program on sleep till next class, time left = " + convert(sec_left))
            discord_zindabaad('waiting', y[class_time][0], class_time, y[class_time][1], sec_left)
            sleep(sec_left)
            openClass(y[class_time][0], y[class_time][1])

while True:
    class_schedule()

#THINGS NEED TO IMPORVE
    #ERROR HANDLING
    #DYNAMIC LINK OPENING
    #REMOVE TIME DELAY WITH MORE EFFICIENT CODE
    #REMOVING THE HARD CODING
