"""
Imgur Slideshow script
Script to open Imgur.com and automate viewing of the pages and images
By Pete Lock (petelock@gmail.com)
Disclaimer
This script, or the author, are in no way connected to the Imgur Company.
Imgur have no knowledge of this and have not given any type of approval.
"""
import sys
import os
import time
from selenium import webdriver
import urllib3
import re

# See http://selenium-python.readthedocs.io/installation.html
# or similar for installation details

####### Options
time_On_Each_Image = 8 # Seconds
time_On_Comment = 8 # Seconds
imgur_Flavour = 1 # See below for imgur_Flavours

usr = ''
# Change to suit your environment
install_dir = ''
if sys.platform.startswith('win32'):
    usr = os.environ['USERNAME']
    install_dir = 'C:\\Users\\' + usr + '\\Documents\\imgur' # 
elif sys.platform.startswith('darwin'):
    usr = os.environ['USER']
    install_dir = '/Users/' + usr + '/Documents/imgur'
elif sys.platform.startswith('linux'):
    usr = os.environ['USER']
    install_dir = '/home/' + usr + '/Documents/imgur'
    
# Ad Blocker - note: this script was developed with an Ad Blocker enabled. 
# If you dont use one then you may need to increase the timings above
# If you do not want to use an AdBlocker, set use_adBlocker to 0
use_adBlocker = 1
# If you want to use an AdBlocker change the following to suit your environment
if use_adBlocker:
    if sys.platform.startswith('win32'):
        adBlockLocation = install_dir + '\\uBlock-Origin_v1.11.0.crx' # Change to suit your environment
    elif sys.platform.startswith('darwin'):
        adBlockLocation = install_dir + '/uBlock-Origin_v1.11.0.crx'
    elif sys.platform.startswith('linux'):
        adBlockLocation = install_dir + '/uBlock-Origin_v1.11.0.crx'
    

####### End of Options

def makeChoices():
    flavour = input("Which flavour of Imgur would you like to browse? (1): ")
    image_time = input("Time for each Image to be displayed (in seconds) (12): ")
    comment_time = input("Time for comments to be displayed (in seconds) (12): ")
    if flavour=='':flavour=1
    if image_time=='':image_time=12
    if comment_time=='':comment_time=12
    return flavour, image_time, comment_time

if ( len(sys.argv) ) > 1:
    flavas = ["Imgur","Most Viral (popularity)","Most Viral (newest first)","Most Viral (today) ","Most Viral (this week) ","Most Viral (this month) ","Most Viral (this year) ","Most Viral (all time) ","UserSub (popularity)","UserSub (newest first)","UserSub (rising)","Funny","The More You Know","Science and Tech","Gaming","Eat What You Want","Aww","Inspiring","Awesome","Creativity","The Great Outdoors","Storytime","Movies and TV","Reaction","Current Events","Staff Picks","A Day In The Life","Uplifting"]
    if str(sys.argv[1]) == '-opt':
        print("Imgur Slideshow Options")
        cnt=0
        for flava in flavas:
            if cnt>0:
                out = str(cnt) + ": " + flavas[cnt]
                print (out)
            cnt += 1 
        
        flavour = 0
        image_time = 0
        comment_time = 0
        
        choices = 0
        while choices < 1:
            flavour,image_time,comment_time = makeChoices()
            # Check user input
            try:
                imgur_Flavour = int(flavour)
            except: 
                imgur_Flavour = 'fail'
            try:
                time_On_Each_Image = float(image_time)
            except: 
                time_On_Each_Image = 'fail'
            try:
                time_On_Comment = float(comment_time)
            except: 
                time_On_Comment = 'fail'
            if ((isinstance(imgur_Flavour,int)) and (imgur_Flavour>0) and (imgur_Flavour<28)
                 and (isinstance(time_On_Each_Image,float)) and (isinstance(time_On_Comment,float))):
                choices = 1
            else:
                print("Ooops - Values not numbers or out of range, have another go...")
        
        print(imgur_Flavour)
        print("---------------------------------")    
        print("Starting Imgur automated browsing")
        print("Flavour ",flavas[int(imgur_Flavour)], "(",imgur_Flavour,")",sep='')
        print("Image timing ",image_time,"seconds")
        print("Comment time of",time_On_Comment,"seconds")
        print("---------------------------------")
        time.sleep(3)
    else:
        print("Usage: \npython imgur.py\t\t(to use default options)\npython imgur.py -opt\t(to change timing options)\n")
        sys.exit(0)

def imgurFlavour(imgur_Flavour):
    if imgur_Flavour == 1: return 'http://imgur.com/hot/viral' # Most Viral (popularity)
    if imgur_Flavour == 2: return 'http://imgur.com/hot/time' # Most Viral (newest first)
    if imgur_Flavour == 3: return 'http://imgur.com/top' # Most Viral (today) 
    if imgur_Flavour == 4: return 'http://imgur.com/top/viral/week' # Most Viral (this week) 
    if imgur_Flavour == 5: return 'http://imgur.com/top/viral/month' # Most Viral (this month) 
    if imgur_Flavour == 6: return 'http://imgur.com/top/viral/year' # Most Viral (this year) 
    if imgur_Flavour == 7: return 'http://imgur.com/top/viral/all' # Most Viral (all time) 
    if imgur_Flavour == 8: return 'http://imgur.com/new/viral' # UserSub (popularity)
    if imgur_Flavour == 9: return 'http://imgur.com/new/time' # UserSub (newest first)
    if imgur_Flavour == 10: return 'http://imgur.com/new/rising' # UserSub (rising)


    if imgur_Flavour>10:
        url = 'http://imgur.com/topic/' + flavas[imgur_Flavour]
        url.replace(" ", "_")
        return url


# Set up Selenium Webdriver
chr_opt = webdriver.ChromeOptions()
if sys.platform.startswith('win32'):
    chr_opt.add_argument("user-data-dir=C:\\Users\\" + usr + "\\AppData\\Local\\Google\\Chrome\\User");
elif sys.platform.startswith('darwin'):
    chr_opt.add_argument("user-data-dir=/Users/" + usr + "/Library/Application Support/Google/Chrome/Default");    
elif sys.platform.startswith('linux'):
    chr_opt.add_argument("user-data-dir=/home/" + usr + "/.config/google-chrome/Default");

if (use_adBlocker):
    chr_opt.add_extension(adBlockLocation)  

if sys.platform.startswith('win32'):
    driver = webdriver.Chrome(executable_path=install_dir + '\\chromedriver.exe', chrome_options=chr_opt)
elif sys.platform.startswith('darwin'):
    driver = webdriver.Chrome(executable_path=install_dir + 'chromedriver', chrome_options=chr_opt)
elif sys.platform.startswith('linux'):
    driver = webdriver.Chrome(executable_path=install_dir + '/chromedriver', chrome_options=chr_opt)

# Go to your selected list, uncomment one of the following
driver.get(imgurFlavour(imgur_Flavour)) 
driver.set_window_position(1400, 200)
driver.set_window_size(880, 920)
driver.maximize_window()
time.sleep(3)

# Clear the User Sub warning if neccesary
if len(driver.find_elements_by_id('gallery-new-info-okay')) > 0:
    content = driver.find_element_by_id('gallery-new-info-okay').click()
    time.sleep(3)

# Click on the first image
content = driver.find_element_by_class_name('image-list-link').click()
time.sleep(16)

def getImages(drv,elem):
    return driver.find_elements_by_class_name(elem)

def addUniq(pi_ids,elem):
    if elem not in pi_ids:
        pi_ids.append(elem)
        
def showStats(img):
    print("showing: http://imgur.com/",img.get_attribute('id'),' ',sep='',end=' ')
    #print(img.location)
    print(img.size)
    
def getFileSize(img,drv):
    # This function tries to work out the size of a file and if its a video to add a pause to the 
    # viewing dispaly time if its over a certain size. It only works moderaterly well and badly 
    # optimized GIFs can be short but with a large file size, but I tried.
    
    ps = drv.page_source
    regex = re.escape(img.get_attribute('id')) + r".(\w+)"
    matches = re.findall(regex, ps)
#     for match in matches:
#         print (match)
    
    ty = ''
    
    if 'mp4' in matches:
        ty = 'mp4'
    if 'gif' in matches:
        ty = 'gif'
    if 'gifv' in matches:
        ty = 'gifv'
    
    delay = 0
    
    if ty != '':
        http = urllib3.PoolManager()
        imgURL = "http://i.imgur.com/" + img.get_attribute('id') + '.' + ty
#         print (imgURL)
        r = http.request('GET', imgURL)
        hds = r.headers
        
        regex = r"Content-Length'\: '(\d+)"
        matches = re.findall(regex, str(r.headers))
        for match in matches:
#             print (match)
            delay = int(int(match)/128000)
#             print (delay)
            if delay>1:
                time.sleep(delay)

def updateLists():
    
    global post_images
    global post_images_ids
    global all_images_ids
    global next_image_ids
    global all_posts
    
    # Get images on the page at this point
    post_images = getImages(driver, 'post-image-container')
    #print (len(post_images), " image/s on the page at this point")

    # Build list of images ids currently on the page
    post_images_ids = []
    for img in post_images:
        post_images_ids.append(img.get_attribute('id'))

    # Find next images on the page
    next_image_ids = []
    for imgid in post_images_ids:
         if imgid not in all_images_ids:
             next_image_ids.append(imgid)

    # Add current images to all_posts
    for img in post_images:
        addUniq(all_posts, img)

    # Add current images ids to all_images_ids
    for img in next_image_ids:
        addUniq(all_images_ids, img)


count = 0
# Loop thru the Posts
while (count < 1):
    #print("New page --- ", driver.current_url)

    all_posts = []
    pi_ids = []
    cnt = 0

    # For initial state of page
    post_images = getImages(driver, 'post-image-container')
    
    for i in post_images:
        addUniq(all_posts, i)
    time.sleep(2)

    # Build list of all images initially on the page
    all_images_ids = []
    for img in all_posts:
        all_images_ids.append(img.get_attribute('id'))

    # Scroll thru initial images
    #print("Scrolling thru the initial image/s available")
    for img in post_images:
        #showStats(img)
        getFileSize(img,driver)
        img.location_once_scrolled_into_view
        time.sleep(time_On_Each_Image)

    page_done = 0
    while (page_done < 1):

        updateLists()
        
        # If there are no more images to show
        if not next_image_ids:
            # Open up extra images if available
            if len(driver.find_elements_by_class_name('js-post-truncated')) > 0:
                #print("Opening up extra images")
                load_more = driver.find_element_by_class_name('js-post-truncated').click()
                time.sleep(6)

                updateLists()

            else:
                # Jump to Comments
                comments = driver.find_element_by_class_name('comments-info')
                comments.location_once_scrolled_into_view
                driver.execute_script("window.scrollBy(0, 400);")
                #print ("Scrolling to Comments")
                time.sleep(time_On_Comment)
                # Go to next page
                next_post_btn = driver.find_element_by_class_name('navNext').click()
                time.sleep(16)
                break


        cnt = 0
        # Scroll to next image
        #print("Scrolling thru the next image/s available")
        for img in post_images:
            if img.get_attribute('id') == next_image_ids[cnt]:
                #showStats(img)
                img.location_once_scrolled_into_view
                time.sleep(time_On_Each_Image)
                cnt += 1
                if cnt > len(next_image_ids):
                    break


