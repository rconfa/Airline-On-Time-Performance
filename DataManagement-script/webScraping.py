import glob
import os
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from zipfile import ZipFile

downloadsPath = './/download'
# create a new directory for download
if not os.path.exists(downloadsPath):
    os.makedirs(downloadsPath)

# change the default download directory
def set_download_dir():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    prefs = {"profile.default_content_settings.popups": 0,
             "download.default_directory": r"C:\Users\Riccardo\Desktop\DataManIntegration\download",
             "directory_upgrade": True,
             "download.prompt_for_download": False,
             "safebrowsing.enabled": True,
             'profile.default_content_setting_values.automatic_downloads': 1}
    options.add_experimental_option("prefs", prefs)
    return options

def select_chechboxes():
    # get all checkbox items
    checkboxList = browser.find_elements_by_xpath('//*[@id="VarName"]')
    # click on all elements I need
    checkboxList[0].click()  # Year
    checkboxList[2].click()  # month
    checkboxList[3].click()  # Day of Month
    checkboxList[4].click()  # Day of week
    checkboxList[8].click()  # IATA_CODE_Reporting_Airline
    checkboxList[14].click()  # Origin
    checkboxList[15].click()  # OriginCityName
    checkboxList[18].click()  # OriginStateName
    checkboxList[23].click()  # Dest
    checkboxList[24].click()  # DestCityName
    checkboxList[27].click()  # DestStateName
    checkboxList[29].click()  # CRSDepTime
    checkboxList[30].click()  # DepTime
    checkboxList[31].click()  # DepDelay
    checkboxList[34].click()  # DepartureDelayGroups
    checkboxList[40].click()  # CRSArrTime
    checkboxList[41].click()  # ArrTime
    checkboxList[42].click()  # ArrDelay
    checkboxList[45].click()  # ArrivalDelayGroups
    checkboxList[47].click()  # Cancelled
    checkboxList[48].click()  # CancellationCode
    checkboxList[49].click()  # Diverted
    checkboxList[50].click()  # CRSElapsedTime
    checkboxList[51].click()  # ActualElapsedTime
    checkboxList[52].click()  # AirTime
    checkboxList[54].click()  # Distance
    checkboxList[55].click()  # DistanceGroup
    checkboxList[56].click()  # CarrierDelay
    checkboxList[57].click()  # WeatherDelay
    checkboxList[58].click()  # NASDelay
    checkboxList[59].click()  # SecurityDelay
    checkboxList[60].click()  # LateAircraftDelay

    # remove pre-checked element that are unused
    browser.execute_script("arguments[0].click();", checkboxList[11])  # OriginAirportID
    browser.execute_script("arguments[0].click();", checkboxList[12])  # OriginAirportSeqID
    browser.execute_script("arguments[0].click();", checkboxList[13])  # OriginCityMarketID
    browser.execute_script("arguments[0].click();", checkboxList[20])  # DestAirportID
    browser.execute_script("arguments[0].click();", checkboxList[21])  # DestAirportSeqID
    browser.execute_script("arguments[0].click();", checkboxList[22])  # DestCityMarketID

# wait till download end
def wait_for_downloads():
    print("Waiting for downloads", end="")
    while any([filename.endswith(".crdownload") for filename in
               os.listdir(downloadsPath)]):
        time.sleep(3)
        print(".", end="")
    print("done!")

def download_file(btn_download):
    # download file
    browser.execute_script("arguments[0].click();", btn_download)
    time.sleep(3)  # little sleep, I need to wait before the file .crdownload is really create
    # waiting till the download is ended
    wait_for_downloads()

def extract_rename_zip(new_filename):
    # handle the .zip downloaded, I'm sure that there is only one .zip file each time
    fileList = glob.glob(downloadsPath + "\*.zip")

    # opening the zip file in READ mode
    with ZipFile(fileList[0], 'r') as zip:
        # get the csv filename
        oldName = downloadsPath + "\\" + zip.namelist()[0]

        # extracting all the files
        print('Extracting all the files now...', end="")
        zip.extractall(downloadsPath)
        print('done!')

    # renaming the extracted .csv file
    os.rename(oldName, new_filename)
    # removing the .zip folder
    os.remove(fileList[0])


# browser object
browser = webdriver.Chrome(options=set_download_dir())

# access to the page
browser.get('https://www.transtats.bts.gov/Tables.asp?QO_VQ=EFD&QO_anzr=Nv4yv0r%FDb0-gvzr%FDcr4s14zn0pr%FDQn6n'
            '&QO_fu146_anzr=b0-gvzr')
# go to download page
btn = browser.find_element_by_xpath(
    '/html/body/div[3]/div[3]/table/tbody/tr/td[2]/form/table[3]/tbody/tr[7]/td[2]/a[3]').click()

# select all info that I need to download
select_chechboxes()

# get the selection for year and month
yearSelector = Select(browser.find_element_by_xpath('//*[@id="XYEAR"]'))  # option selector for year
monthSelector = Select(browser.find_element_by_xpath('//*[@id="FREQUENCY"]'))  # option selector for month

# get the download button
btnDownload = browser.find_element_by_xpath("/html/body/div[3]/div[3]/table[1]/tbody/tr/td[2]/table[3]/tbody/tr/td["
                                            "2]/button[1]")

# get the 2018-19 .csv for all month!
for intYear in range(2018, 2020):
    # setting the value for the year option
    yearSelector.select_by_value(str(intYear))
    for intMonth in range(1, 13):
        # setting the value for the month option
        monthSelector.select_by_value(str(intMonth))
        # get the corresponding file
        download_file(btnDownload)
        # set the new file name
        newFilename = downloadsPath + "\\" + str(intYear) + "_" + str(intMonth) + ".csv"
        extract_rename_zip(newFilename)

# closing the web page
browser.close()
