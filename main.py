# Copyright (c) 2024, Kuronekosan
# This version is still alpha-release

import os
import sys
from time import sleep
from dotenv import load_dotenv
from utils.dataExtract import ExtractData
from playwright.sync_api import sync_playwright

load_dotenv()

if not ( os.getenv('ML_USER') and os.getenv('ML_PASSWORD') ):
    print("Please check your .env file!")
    sys.exit(1)

extractFunc = ExtractData()
date = input('DATE (Format: YYYY-MM-DD): ')
cat = input('\nCATEGORY (Format: U10/U12): ')
typed = input('\nTYPE (Format: T/FG/SC): ')

if cat not in ['U10', 'U12'] or typed not in ['T', 'FG', 'SC']:
    print("This feature is not developed yet.")
    sys.exit(1)

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context(storage_state='./auth.json',viewport={"width": 1366, "height": 768}) if os.path.exists('./auth.json') else browser.new_context(viewport={"width": 1366, "height": 768})
    page = context.new_page()
    
    if not os.path.exists('./auth.json'):
        page.goto('https://admin.milklifesoccer.com/#/aksimayaAuth/login')
        sleep(2)
        page.get_by_placeholder("Username").fill( os.getenv('ML_USER') )
        sleep(1)
        page.get_by_placeholder("Password").fill( os.getenv('ML_PASSWORD') )
        sleep(1)
        page.get_by_role("button", name="Log in").click()
        sleep(3)
    else:
        page.goto('https://admin.milklifesoccer.com/#/app/home')
        sleep(1)

    try:
        page.locator('//*[@id="header"]/div[2]/ul[1]/li').click()
    except:
        print("Failed to Login, please check the username and password on .env and check your internet connection")
        sys.exit(1)

    sleep(1)
    page.locator("//html/body/div[4]/div/div[2]/div/div/div/a[3]").click()
    sleep(2)
    if not os.path.exists('./auth.json'):
        page.context.storage_state(path='./auth.json')
        sleep(2)
    page.goto('https://admin.milklifesoccer.com/#/view/matches/')
    sleep(2)
    pw.selectors.set_test_id_attribute("ng-model")
    page.get_by_test_id("vm.adv.plandate").select_option(value='{v}'.format(v = date))
    sleep(1)
    # pw.selectors.set_test_id_attribute("ng-model")
    page.get_by_test_id("vm.adv.kategori").select_option(value='{v}'.format(v = 'U10' if cat == 'U10' else 'U12' if cat == 'U12' else 'Semua'))
    sleep(1)
    # pw.selectors.set_test_id_attribute("ng-model")
    page.get_by_test_id("vm.adv.draw_type").select_option(value='{v}'.format(v = '1' if typed == 'T' else '2' if typed == 'FG' else '3' if typed == 'SC' else 'All'))
    sleep(7)
    pw.selectors.set_test_id_attribute("ng-repeat")
    totalData = page.get_by_test_id("row in vm.tableSvc.datas | filter:vm.filterKey")
    sleep(1)
    if totalData.count() == 0:
        print("Data is empty.")
        sys.exit(1)

    if typed == 'SC':
        loopStepper = extractFunc.stepper(totalData.count(), 5)

        for row in range( len(loopStepper) ):
            data = ""
            lFirst = loopStepper[row]['first']
            lLast = loopStepper[row]['last']
            loc = extractFunc.cap( totalData.nth(0).locator('td').nth(1).inner_text().split('-',1)[0] )
            title = "{t} - {l} {c},{d}".format(t = 'SKILL CHALLENGE' if typed == 'SC' else '7 x 7' if typed == 'FG' else 'TOURNAMENT', l = loc, c = cat, d = extractFunc.extractDate(date, 1))
            
            for nRow in range(lFirst, lLast+1):
                loc, loc_i = extractFunc.cap( totalData.nth(nRow).locator('td').nth(1).inner_text() ).split('-')
                if nRow == lFirst:
                    data += "{ttl},{t},{d},{t1},{t2},{r}".format( ttl = title, t = extractFunc.extractTime(totalData.nth(nRow).locator('td').nth(2).inner_text()), d = extractFunc.extractDraw(totalData.nth(nRow).locator('td').nth(4).inner_text(), cat + " "), t1 = extractFunc.extractPlayers(totalData.nth(nRow).locator('td').nth(7).inner_text(), " " + cat), t2 = extractFunc.extractPlayers(totalData.nth(nRow).locator('td').nth(9).inner_text(), " " + cat), r = extractFunc.cap(totalData.nth(nRow).locator('td').nth(11).inner_text()) )
                else:
                    data += ",{t},{d},{t1},{t2},{r}".format( t = extractFunc.extractTime(totalData.nth(nRow).locator('td').nth(2).inner_text()), d = extractFunc.extractDraw(totalData.nth(nRow).locator('td').nth(4).inner_text(), cat + " "), t1 = extractFunc.extractPlayers(totalData.nth(nRow).locator('td').nth(7).inner_text(), " " + cat), t2 = extractFunc.extractPlayers(totalData.nth(nRow).locator('td').nth(9).inner_text(), " " + cat), r = extractFunc.cap(totalData.nth(nRow).locator('td').nth(11).inner_text()) )
            print("\n\n",data)
            extractFunc.extractToCsv(data, date, cat, typed, "{d}_{c}_{t}_{l}".format( d = date, c = cat, t = typed, l = row ))

    elif typed == 'FG':
        loopStepper = extractFunc.stepper(totalData.count(), 4)

        for row in range( len(loopStepper) ):
            data = ""
            lFirst = loopStepper[row]['first']
            lLast = loopStepper[row]['last']
            loc = extractFunc.cap( totalData.nth(0).locator('td').nth(1).inner_text().split('-',1)[0] )
            title = "{t} - {l} {c},{d}".format(t = 'SKILL CHALLENGE' if typed == 'SC' else '7 x 7' if typed == 'FG' else 'TOURNAMENT', l = loc, c = cat, d = extractFunc.extractDate(date, 1))

            for nRow in range(lFirst, lLast+1):
                loc, loc_i = extractFunc.cap( totalData.nth(nRow).locator('td').nth(1).inner_text() ).split('-')
                if nRow == lFirst:
                    data += "{titl},{t},{c},{l},{t1},{t2},{g}".format( titl = title, t = extractFunc.extractTime(totalData.nth(nRow).locator('td').nth(2).inner_text()), c = totalData.nth(nRow).locator('td').nth(0).inner_text(), l = 'REN-{i}'.format(i = loc_i) if loc == 'RENDENG' else 'SSA-{i}'.format(i = loc_i), t1 = extractFunc.extractPlayersFG(totalData.nth(nRow).locator('td').nth(7).inner_text(), " " + cat), t2 = extractFunc.extractPlayersFG(totalData.nth(nRow).locator('td').nth(9).inner_text(), " " + cat), g = totalData.nth(nRow).locator('td').nth(5).inner_text() )
                else:
                    data += ",{t},{c},{l},{t1},{t2},{g}".format( t = extractFunc.extractTime(totalData.nth(nRow).locator('td').nth(2).inner_text()), c = totalData.nth(nRow).locator('td').nth(0).inner_text(), l = 'REN-{i}'.format(i = loc_i) if loc == 'RENDENG' else 'SSA-{i}'.format(i = loc_i), t1 = extractFunc.extractPlayersFG(totalData.nth(nRow).locator('td').nth(7).inner_text(), " " + cat), t2 = extractFunc.extractPlayersFG(totalData.nth(nRow).locator('td').nth(9).inner_text(), " " + cat), g = totalData.nth(nRow).locator('td').nth(5).inner_text() )
            print("\n\n",data)
            extractFunc.extractToCsv(data, date, cat, typed, "{d}_{c}_{t}_{l}".format( d = date, c = cat, t = typed, l = row ))
    else:
        semiFinal = totalData.filter(has = page.get_by_role("cell", name="SF"))
        semiFinalLoc, semiFinalLoc_i = extractFunc.cap( semiFinal.nth(0).locator('td').nth(1).inner_text() ).split('-')
        semiFinalTitle = "{t} - {l} {c},{d}".format( t = 'SEMI FINAL', l = semiFinalLoc, c = cat, d = extractFunc.extractDate(date, 1))

        final = totalData.filter(has = page.get_by_role("cell", name="Final"))
        finalLoc, finalLoc_i = extractFunc.cap( final.nth(0).locator('td').nth(1).inner_text() ).split('-')
        finalTitle = "{t} - {l} {c},{d}".format( t = 'FINAL', l = finalLoc, c = cat, d = extractFunc.extractDate(date, 1))
        data = ""

        for row in range( semiFinal.count() ):

            if row == 0:
                data += "{titl},{t},{c},{l},{t1},{t2}".format( titl = semiFinalTitle, t = extractFunc.extractTime(semiFinal.nth(row).locator('td').nth(2).inner_text()), c = semiFinal.nth(row).locator('td').nth(6).inner_text().replace('#', '', -1), l = 'REN-{i}'.format(i = semiFinalLoc_i) if semiFinalLoc == 'RENDENG' else 'SSA-{i}'.format(i = semiFinalLoc_i), t1 = extractFunc.extractPlayersFG(semiFinal.nth(row).locator('td').nth(7).inner_text(), " " + cat), t2 = extractFunc.extractPlayersFG(semiFinal.nth(row).locator('td').nth(9).inner_text(), " " + cat) )
            else:
                data += ",{t},{c},{l},{t1},{t2}".format( t = extractFunc.extractTime(semiFinal.nth(row).locator('td').nth(2).inner_text()), c = semiFinal.nth(row).locator('td').nth(6).inner_text().replace('#', '', -1), l = 'REN-{i}'.format(i = semiFinalLoc_i) if semiFinalLoc == 'RENDENG' else 'SSA-{i}'.format(i = semiFinalLoc_i), t1 = extractFunc.extractPlayersFG(semiFinal.nth(row).locator('td').nth(7).inner_text(), " " + cat), t2 = extractFunc.extractPlayersFG(semiFinal.nth(row).locator('td').nth(9).inner_text(), " " + cat) )

        print("Data: ", data)
        extractFunc.extractToCsv(data, date, cat, typed, "{d}_{c}_{t}_{l}_SF".format( d = date, c = cat, t = typed, l = row ))
        data = ""

        for row in range( final.count() ):

            if row == 0:
                data += "{titl},{t},{c},{l},{t1},{t2}".format( titl = finalTitle, t = extractFunc.extractTime(final.nth(row).locator('td').nth(2).inner_text()), c = final.nth(row).locator('td').nth(6).inner_text().replace('#', '', -1), l = 'REN-{i}'.format(i = finalLoc_i) if semiFinalLoc == 'RENDENG' else 'SSA-{i}'.format(i = finalLoc_i), t1 = extractFunc.extractPlayersFG(final.nth(row).locator('td').nth(7).inner_text(), " " + cat), t2 = extractFunc.extractPlayersFG(final.nth(row).locator('td').nth(9).inner_text(), " " + cat) )
            else:
                data += ",{t},{c},{l},{t1},{t2}".format( t = extractFunc.extractTime(final.nth(row).locator('td').nth(2).inner_text()), c = final.nth(row).locator('td').nth(6).inner_text().replace('#', '', -1), l = 'REN-{i}'.format(i = finalLoc_i) if semiFinalLoc == 'RENDENG' else 'SSA-{i}'.format(i = finalLoc_i), t1 = extractFunc.extractPlayersFG(final.nth(row).locator('td').nth(7).inner_text(), " " + cat), t2 = extractFunc.extractPlayersFG(final.nth(row).locator('td').nth(9).inner_text(), " " + cat) )


        print("Data: ", data)
        extractFunc.extractToCsv(data, date, cat, typed, "{d}_{c}_{t}_{l}_FINAL".format( d = date, c = cat, t = typed, l = row ))

    sleep(5)