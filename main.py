import os, sys, time, threading, configparser, datetime

from web3 import Web3

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.uic import *

ETHER = 1000000000000000000
MAIN_ACCOUT = "0xc9be19ea7da2bb8fbf12fc8c170d243080597d8e"
reader = configparser.ConfigParser()

class GethConnector():
    def __init__(self):
        self.wb3 = Web3(Web3.HTTPProvider("http://192.168.21.108:8545"))
        self.isConnected()
        self.loginAccount(MAIN_ACCOUT, "000")

    def isConnected(self):
        print(self.wb3.isConnected())

    def loginAccount(self, account, password):
        account = self.wb3.toChecksumAddress(account)
        self.wb3.geth.personal.unlockAccount(account, password)
        self.wb3.eth.defaultAccount = account

class system():
    def start(self):
        reader.read("./data/contract.ini")
        self.ca = reader.get("DATA", "address")
        self.cabi = reader.get("DATA", "abi")
        self.cc = w.wb3.eth.contract(abi = self.cabi, address = self.ca)

    #Отправить сумму от аккаунта к аккаунту
    def transfer(self, address_from, address_to, value, grade = "wei"):
        trans = w.wb3.eth.sendTransaction({"from": w.wb3.toChecksumAddress(address_from), "to": w.wb3.toChecksumAddress(address_to), "value": w.wb3.toWei(value, grade)})
        w.wb3.eth.waitForTransactionReceipt(trans)

    #зарегистрировать владельца
    def driverRegistration(self, login, fullName, blockchainAddress):
        trans = self.cc.functions.driverRegistration(login, fullName, blockchainAddress).transact()
        w.wb3.eth.waitForTransactionReceipt(trans)

    #добавить ВУ водителю
    def addDriverLicense(self, driver, number, validity, category):
        trans = self.cc.functions.addDriverLicense(driver, number, validity, category, 0).transact()
        w.wb3.eth.waitForTransactionReceipt(trans)

    #продлить ВУ
    def continueDirverLicense(self, number, newValidity):
        trans = self.cc.functions.continueDirverLicense(number, newValidity).transact()
        w.wb3.eth.waitForTransactionReceipt(trans)

    #зарегистрировать ТС водителю
    def transportRegistration(self, driver, category, price, lifeTime, name):
        trans = self.cc.functions.transportRegistration(driver, category, price, lifeTime, name).transact()
        w.wb3.eth.waitForTransactionReceipt(trans)

    #оформить страховку
    def takeToInsuranceFee(self, driver, value):
        trans = self.cc.functions.takeToInsuranceFee(driver, value).transact()
        w.wb3.eth.waitForTransactionReceipt(trans)

    #заплатить штраф по номеру
    def payFine(self, number):
        paytime = int(time.time())
        trans = self.cc.functions.payFine(number, paytime).transact()
        w.wb3.eth.waitForTransactionReceipt(trans)

    #оформить штраф
    def formFine(self, number, date, tim, text):
        formtime = int(time.time())
        trans = self.cc.functions.formFine(number, text, date, tim, formtime).transact()
        w.wb3.eth.waitForTransactionReceipt(trans)

    #оформить дтп
    def formAccident(self, number, suma, text, date, time):
        trans = self.cc.functions.formAccident(number, suma, text, date, time).transact()
        w.wb3.eth.waitForTransactionReceipt(trans)

    #продлить опыт вождения водителю
    def setDrivingExpirience(self, login, value):
        trans = self.cc.functions.setDrivingExpirience(login, value).transact()
        w.wb3.eth.waitForTransactionReceipt(trans)

    #Добавить долг компании
    def addDebtCompany(self, value):
        trans = self.cc.functions.addDebtCompany(value).transact()
        w.wb3.eth.waitForTransactionReceipt(trans)

    #Обнулить долг компании
    def setEmptyDebtCompany(self):
        trans = self.cc.functions.setEmptyDebtCompany().transact()
        w.wb3.eth.waitForTransactionReceipt(trans)
       
    #Отнять долг у компании
    def subtractDebtCompany(self, value):
        trans = self.cc.functions.subtractDebtCompany(value).transact()
        w.wb3.eth.waitForTransactionReceipt(trans)

    #оплатить определённый штраф
    def payOneFine(self, index):
        trans = self.cc.functions.payOneFine(index).transact()
        w.wb3.eth.waitForTransactionReceipt(trans)

    #информация об владельце
    def getUserInfo(self, login):
        ret = self.cc.functions.getUserInfo(login).call()
        return ret

    #информация об ВУ
    def getDriverLicenseInfo(self, number):
        ret = self.cc.functions.getDriverLicenseInfo(number).call()
        return ret

    #есть ли лицензия у водителя
    def isThereDriverLicense(self, driver):
        ret = self.cc.functions.isThereDriverLicense(driver).call()
        return ret

    #занята ли лицензия
    def isThereDriverLicenseBusy(self, number):
        ret = self.cc.functions.isThereDriverLicenseBusy(number).call()
        return ret

    #узнать об транспорте у водителя
    def getTransportInfo(self, driver):
        ret = self.cc.functions.getTransportInfo(driver).call()
        return ret

    #есть ли транспорт у водителя
    def isTransportThere(self, driver):
        ret = self.cc.functions.isTransportThere(driver).call()
        return ret

    #есть ли страховка у водителя
    def isThereInsurance(self, driver):
        ret = self.cc.functions.isThereInsurance(driver).call()
        return ret

    #узнать всё о штрафе
    def getFineInfo(self, index):
        ret = self.cc.functions.getFineInfo(index).call()
        return ret

    #история дтп
    def getAccidentInfo(self, index):
        ret = self.cc.functions.getAccidentInfo(index).call()
        return ret

    #Получить общее количество ДТП
    def getTotalAccidentsCount(self):
        ret = self.cc.functions.getTotalAccidentsCount().call()
        return ret

    #Получить общее количество штрафов    
    def getTotalFinesCount(self):
        ret = self.cc.functions.getTotalFinesCount().call()
        return ret

    #Получить Сумма всех штрафов водителя    
    def getAllFinesSum(self, driver):
        ret = self.cc.functions.getAllFinesSum(driver).call()
        return ret

    #Получить количество штрафов водителя
    def getDriverFinesCount(self, driver):
        ret = self.cc.functions.getDriverFinesCount(driver).call()
        return ret

    def getFineTimeStamp(self, index):
        ret = self.cc.functions.getFineTimeStamp(index).call()
        return ret
    
    def getCompanyDebt(self):
        ret = self.cc.functions.getCompanyDebt().call()
        return ret

    def isThereDriverLicenseConfirmed(self, number):
        ret = self.cc.functions.isThereDriverLicenseConfirmed(number).call()
        return ret

    def getDriverNoPaybleFinesCount(self, driver):
        ret = self.cc.functions.getDriverNoPaybleFinesCount(driver).call()
        return ret
    
    def getDriverPaybleFinesCount(self, driver):
        ret = self.cc.functions.getDriverPaybleFinesCount(driver).call()
        return ret

class into(QWidget):
    def __init__(self, *argc):
        super(into, self).__init__(*argc)
        loadUi("./forms/into.ui", self)
        self.reg_close.clicked.connect(self.cancelButtonPressed)
        self.log_b.clicked.connect(self.logButtonPressed)
        self.reg_b.clicked.connect(self.regButtonPressed)
        self.setupUI()
        s.start()

    def setupUI(self):
        self.reg_input_f.hide()
        self.reg_buttons_f.hide()
        self.show()

    def cancelButtonPressed(self):
        self.reg_input_f.hide()
        self.reg_buttons_f.hide()
        self.log_buttons_f.show()
        self.login.clear()
        self.password.clear()
        self.password_again.clear()
        self.name_first.clear()
        self.name_second.clear()

    def logButtonPressed(self):
        data = s.getUserInfo(self.login.text())
        self.f = str(data[5])
        try:
            w.loginAccount(data[5], self.password.text())
        except Exception as e:
            QMessageBox.about(self, "Внимание!","Неверный логин/пароль!")
        else:
            self.selectAccount(data[6])

    def selectAccount(self, role):
        if role == 0: self.isDriverForm()
        elif role == 1: self.isWorkerForm()
        elif role == 2: self.isAdminForm(1)
        elif role == 3: self.isAdminForm(0)
        else: QMessageBox.about(self, "Внимание!","Роль у пользователя не определена!")

    def regButtonPressed(self):
        login = self.login.text()
        fio = self.name_first.text() + " " + self.name_second.text()
        if (self.password.text() != self.password_again.text()):
            QMessageBox.about(self, "Внимание!","Пароли не совпадают!")
        elif (login == "" or fio == " " or self.password.text() == ""):
            QMessageBox.about(self, "Внимание!", "Поля не должны быть пустыми!")
        else:
            try:
                #Создание аккаунта и отправка даненых в контракт
                QMessageBox.about(self, "Внимание!","Может длиться до минуты!\nПодождите пожалуйста!")
                address = w.wb3.geth.personal.newAccount(self.password.text())
                s.driverRegistration(login, fio, address)
                s.transfer(MAIN_ACCOUT, address, 50, "ether")
            except Exception as e:
                QMessageBox.about(self, "Внимание!", "Неожиданная ошибка при регистрации:\n" + str(e) + "\nОбратитесь за помощью к программисту!")
            else:
                self.cancelButtonPressed()
                QMessageBox.about(self, "Внимание!","Готово, теперь войдите в ваш аккаунт!")

    def isAdminForm(self, role):
        self.f = admin(role, self.f)
        self.close()

    def isDriverForm(self):
        self.f = drv(self.login.text())
        self.close()

    def isWorkerForm(self):
        self.f = dps()
        self.close()

    def showme(self):
        self.show()

class admin(QWidget):
    def __init__(self, status, adress, *argc):
        super(admin, self).__init__(*argc)
        loadUi("./forms/admin.ui", self)
        self.address.setText(adress)
        self.st = status
        self.ad = adress

        self.back_b.clicked.connect(self.isClosed)

        asy = threading.Thread(target=self.balance, args=())
        asy.start()

        asy2 = threading.Thread(target=self.deptCompany, args=())
        asy2.start()

        self.setupUI()

    def isClosed(self):
        log.showme()

    def balance(self):
        time.sleep(2)
        while(True):
            if (self.isVisible() != True): break
            self.ad_bal.setText(str(w.wb3.eth.getBalance(self.ad) / ETHER) + " eth.")
            time.sleep(1)
    
    def deptCompany(self):
        time.sleep(2)
        while(True):
            if (self.isVisible() != True): break
            dept = float(s.getCompanyDebt())
            if (dept < w.wb3.eth.getBalance(s.getUserInfo("company")[5]) and dept != 0.0):
                try:
                    self.company_dept.show()
                    self.company_dept.setText("Производится выплата долга страховой компании")
                    w.loginAccount(s.getUserInfo("company")[5], "000")
                    s.transfer(s.getUserInfo("company")[5], MAIN_ACCOUT, dept)
                    w.loginAccount(MAIN_ACCOUT, "000")
                    s.setEmptyDebtCompany()
                except Exception as e:
                    self.company_dept.setText("Существуют проблеммы с выплатой долга компании: " + str(e))
                    time.sleep(7)
                    self.company_dept.hide()
                else:
                    self.company_dept.setText("Долг Страховой компании был прощён, сумма выплаты (eth): " + str(dept / ETHER))
                    time.sleep(7)
                    self.company_dept.hide()
            time.sleep(5)

    def setupUI(self):
        self.company_dept.hide()
        if self.st == 0: self.isBank()
        elif self.st == 1: self.isIns()
        self.show()

    def isBank(self):
        self.status.setText("Банк")
        self.setWindowTitle("Форма Банка")

    def isIns(self):
        self.status.setText("Страховая компания")
        self.setWindowTitle("Форма страховой компании")

class drv(QWidget):
    def __init__(self, log, *argc):
        super(drv, self).__init__(*argc)
        loadUi("./forms/drv.ui", self)
        self.login = log

        self.exit_b.clicked.connect(self.exitClicked)
        self.ab.clicked.connect(self.aboutClicked)
        self.accept_ins.clicked.connect(self.addInsurance)
        self.accept_vu.clicked.connect(self.setDriverLicense)
        self.accept_ex.clicked.connect(self.setDriverExpirience)
        self.accept_ts.clicked.connect(self.addTransport)
        self.check_fi.clicked.connect(self.checkFine)
        self.pay_fi.clicked.connect(self.payfine)
        self.update_hi_fi.clicked.connect(self.getFinesHistory)
        self.hi_upd_dtp.clicked.connect(self.getAccidentsHistory)

        asy = threading.Thread(target=self.balance, args=())
        asy.start()

        self.ad = s.getUserInfo(self.login)[5]

        self.setupUI()

    def balance(self):
        time.sleep(2)
        while(True):
            if (self.isVisible() == False): break
            self.ad_bal.setText(str(w.wb3.eth.getBalance(self.ad) / ETHER) + " eth.")
            time.sleep(1)

    def setupUI(self):
        self.ab_f.hide()
        self.fin_f.hide()
        self.ins_f.hide()
        self.reg_f.hide()
        self.dtp_f.hide()
        self.info_pay_fi.hide()
        self.whatInsToPay()
        self.history_fi.setText("")
        self.history_dtp.setText("")
        self.show()

    def exitClicked(self):
        self.close()
        log.showme()

    def aboutClicked(self):
        data = s.getUserInfo(self.login)
        self.fio.setText(data[0])
        self.ex_number.setText(str(data[2]))
        self.acc_count.setText(str(data[3]))
        self.address.setText((str(data[5])))
        if (s.isTransportThere(self.login) == False):
            self.cars.setText("У вас нет машин!")
        else:
            trans = s.getTransportInfo(self.login)
            msg = "Машина зарегистрированна!"
            if (trans[3] == False):
                msg = "Машина не зарегистрированна!"
            self.cars.setText("Имя:" + trans[4] + "\nКатегория:" + trans[0] + "\nСрок Службы:" + str(trans[2]) + "\nЦена:" + str(int(trans[1]) / ETHER) + " eth.\n" + msg)
        if (s.isThereInsurance(self.login) == False):
            self.ins_status.setText("У вас нет страховки!")
        else:
            if (data[4] == ''):
                self.ins_status.setText("У вас нет страховки!")
            else:
                self.ins_status.setText(str(float(data[4]) / ETHER))
        if (s.isThereDriverLicense(self.login) == False):
            self.driver_license.setText("У вас нет Водительского удостоверения!")
        else:
            self.driver_license.setText(str(data[1]))
        self.fines_count.setText(str(s.getDriverFinesCount(self.login)))

    def setDriverLicense(self):
        num = self.number_vu.text()
        data = self.date_vu.text()
        cat = self.cat_vu.currentText()
        if (num == ""):
            QMessageBox.about(self, "Внимание!","Введите номер водительского удостоверения!")
        elif (self.is_for_continum_vu.isChecked()):
            val = s.getDriverLicenseInfo(int(num))[0]
            current_driver_license_date = datetime.datetime.strptime(val, "%d.%m.%Y")
            current_driver_license_date_day = int(current_driver_license_date.day)
            current_driver_license_date_month = int(current_driver_license_date.month)
            current_driver_license_date_year = int(current_driver_license_date.year)

            current_date = datetime.datetime.now()
            current_date_day = int(current_date.day)
            current_date_month = int(current_date.month)
            current_date_year = int(current_date.year)

            if current_date_day <= current_driver_license_date_day:
                if current_date_month == current_driver_license_date_month or current_date_month == (current_driver_license_date_month - 1):
                    if current_date_year == current_driver_license_date_year:
                        if current_date_month < 10:
                            current_date_month = '0' + str(current_date_month)
                            new_driver_license_validity = str(str(current_date_day) + '.' + str(current_date_month) + '.' + str(current_date_year + 10))
                            try:
                                s.continueDirverLicense(int(num), new_driver_license_validity)
                            except Exception as e:
                                QMessageBox.about(self, "Ошибка!","Не удалось:\n" + str(e))
                            else:
                                QMessageBox.about(self, "","Успешно!")
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                QMessageBox.about(self, "Ошибка!"," Ваши права не можно продить!")
        
        elif (s.isThereDriverLicenseBusy(int(num))):
            QMessageBox.about(self, "Ошибка!","Ваш номер ВУ уже занят другим пользователем!")
        else:
            try:
                s.addDriverLicense(self.login, int(num), data, cat)
            except Exception as e:
                QMessageBox.about(self, "Ошибка!","Не удалось:\n" + str(e))
            else:
                if (s.isThereDriverLicenseConfirmed(int(num)) == False):
                    QMessageBox.about(self, "Внимание!","Ваш номер ВУ не заригистрован!")
                else:
                    QMessageBox.about(self, "","Успешно!")

    def setDriverExpirience(self):
        ex = self.data_ex.text()
        if (ex == ""):
            QMessageBox.about(self, "Внимание!","Вы должны ввести число!")
        else:
            try:
                s.setDrivingExpirience(self.login, int(ex))
            except Exception as e:
                QMessageBox.about(self, "Ошибка!","Попробуйте попозже!\n" + str(e))
            else:
                QMessageBox.about(self, "Внимение!","Успешно!")

    def addTransport(self):
        name = self.name_ts.text()
        cost = self.cost_ts.text()
        in_use = self.time_ts.text()
        cat = self.cat_ts.currentText()
        if (name == "" or cost == "" or in_use == ""):
            QMessageBox.about(self, "Внимение!","Все поля должны быть заполнены!")
        elif (s.isThereDriverLicense(self.login) == False):
            QMessageBox.about(self, "Ошибка!","Невозможно добавить ТС - у вас нет прав!")
        else:
            try:
                s.transportRegistration(self.login, cat, str(int(cost) * ETHER), int(in_use), name)
            except Exception as e:
                QMessageBox.about(self, "Ошибка!","Попробуйте попозже!\n" + str(e))
            else:
                self.accept_ins.show()
                self.whatInsToPay()
                QMessageBox.about(self, "Внимение!","Успешно!")

    def addInsurance(self):
        if (s.isTransportThere(self.login) == False):
            QMessageBox.about(self, "Ошибка!","У вас нет прав оформлять страховку - нет машины!")
        else:
            try:
                s.takeToInsuranceFee(self.login, str(float(float(self.you_sel.text())) * ETHER))
                s.transfer(s.getUserInfo(self.login)[5], s.getUserInfo("company")[5], float(float(self.you_sel.text())) * ETHER)
            except Exception as e:
                QMessageBox.about(self, "Ошибка!","Попробуйте попозже!\n" + str(e))
            else:
                QMessageBox.about(self, "Внимение!","Успешно!")

    def whatInsToPay(self):
        if (s.isTransportThere(self.login) == False):
            self.you_sel.setText("У вас нет прав оформлять страховку - нет машины!")
            self.accept_ins.hide()
        else:
            trans = s.getTransportInfo(self.login)
            rst = int(trans[1]) / ETHER
            sum_ins = (rst * (1 - trans[2] / 10) * 0.1 + 0.2 * s.getDriverNoPaybleFinesCount(self.login) + s.getUserInfo(self.login)[3] - 0.2 * s.getUserInfo(self.login)[2])
            self.you_sel.setText(str(sum_ins))

    def checkFine(self):
        index = self.num_fi.text()
        self.info_pay_fi.hide()
        if (index == ""):
            QMessageBox.about(self, "Внимание!","Вы должны ввести число!")
        else:
            try:
                info = s.getFineInfo(int(index))
            except Exception as e:
                QMessageBox.about(self, "Ошибка!","Штраф не найден!")
            else:
                if (info[3] != self.login):
                    QMessageBox.about(self, "Ошибка!","Для вашего аккаунта, штрафа с таким номером не найдено!")
                elif (info[6]):
                    self.status_fi.setText("Этот штраф уже оплачен!")
                else:
                    self.date_fi.setText(info[4] + " " + info[5])
                    self.sum_fi.setText(str(float(info[1]) / ETHER))
                    self.comm_fi.setText(info[2])
                    self.info_pay_fi.show()

    def payfine(self):
        index = self.num_fi.text()
        if (index == ""):
            QMessageBox.about(self, "Внимание!","Вы должны ввести число!")
        else:
            try:
                if (s.getFineTimeStamp(int(index)) < int(time.time())):
                    s.transfer(s.getUserInfo(self.login)[5], MAIN_ACCOUT, s.getFineInfo(int(index))[1])
                else:
                    s.transfer(s.getUserInfo(self.login)[5], MAIN_ACCOUT, (float(s.getFineInfo(int(index))[1]) / 2))
                s.payOneFine(int(index))
            except Exception as e:
                QMessageBox.about(self, "Ошибка!","Штраф не был оплачен!\nОшибка:" + str(e))
            else:
                self.info_pay_fi.hide()
                QMessageBox.about(self, "Внимение!","Успешно!")

    def getFinesHistory(self):
        msg = ""
        count = s.getTotalFinesCount()
        number = 0

        while (number != count):
            data = s.getFineInfo(number)
            if(data[3] == self.login):
                msg += " ID: " + str(number) + " Причина штрафа "  + data[2] + ", Статус: "
                if (data[6]):
                    msg += "Оплачен."
                else:
                    msg+= "Не оплачен."
                msg += "Дата и время:" + data[4] + " " + data[5] + "\n" 
            number+=1

        if (msg == ""):
            msg = "Штрафов не найдено!"

        self.history_fi.setText(msg)

    def getAccidentsHistory(self):
        msg = ""
        count = s.getTotalAccidentsCount()
        number = 0

        while (number != count):
            data = s.getAccidentInfo(number)
            if(data[0] == s.getUserInfo(self.login)[1]):
                msg += "Причина ДТП: " + data[2] + ", дата и время: " + data[3] + " " + data[4] + ", сумма ущерба (eth): " + str(float(data[1]) / ETHER) + ".\n"
            number+=1

        if (msg == ""):
            msg = "ДТП не найдены!"

        self.history_dtp.setText(msg)

class dps(QWidget):
    def __init__(self, *argc):
        super(dps, self).__init__(*argc)
        loadUi("./forms/dps.ui", self)

        w.loginAccount(MAIN_ACCOUT, "000")

        self.dtp_accept.clicked.connect(self.isDTP)
        self.fine_accept.clicked.connect(self.isFine)
        self.to_login.clicked.connect(self.intoOpen)
        self.to_drv.clicked.connect(self.drvOpen)

        self.setupUI()

    def setupUI(self):
        self.show()

    def intoOpen(self):
        log.show()

    def drvOpen(self):
        w.loginAccount(s.getUserInfo(log.login.text())[5], log.password.text())
        self.f = drv(log.login.text())

    def isFine(self):
        number = self.fine_drv.text()
        date = self.fine_date.text()
        tim = self.fine_time.text()
        text = self.fine_comm.text()
        if (self.fine_drv.text() == ""):
            QMessageBox.about(self, "Ошибка!","Введите номер водителя!")
        else:
            try:
                s.formFine(int(number), date, tim, text)
            except Exception as e:
                QMessageBox.about(self, "Внимание!","Непредвиденная ошибка:\n" + str(e))
            else:
                QMessageBox.about(self, "Внимание!","Успешно!")

    def isDTP(self):
        number = self.dtp_number.text()
        date = self.dtp_date.text()
        time = self.dtp_time.text()
        text = self.dtp_comm.text()

        if( number == "" ):
            QMessageBox.about(self, "Ошибка!","Введите номер водителя!")
        else:
            try:
                data = s.getDriverLicenseInfo(int(number))
            except Exception as e:
                QMessageBox.about(self, "Водительские права не найдены!","Непредвиденная ошибка:\n" + str(e))
            else:
                if (data[3] == False):
                    QMessageBox.about(self, "Внимание!","Права водителя не подтверждены!")
                else:
                    suma = float(float(s.getUserInfo(data[2])[4]) / ETHER) * 10
                    try:
                        balance = w.wb3.eth.getBalance(s.getUserInfo("company")[5])
                        if (balance < suma):
                            s.transfer(MAIN_ACCOUT, s.getUserInfo("company")[5], suma, "wei")
                            s.addDebtCompany(str(suma))
                        w.loginAccount(s.getUserInfo("company")[5], "000")
                        s.transfer(s.getUserInfo("company")[5], s.getUserInfo(data[2])[5], suma, "wei")
                        s.formAccident(int(number), str(suma), text, date, time)
                    except Exception as e:
                        QMessageBox.about(self, "Ошибка!","Во время оформления ДТП произошла ошибка:\n" + str(e))
                    else:
                        w.loginAccount(MAIN_ACCOUT, "000")
                        QMessageBox.about(self, "Внимание!","Успешно!")
            

app = QtWidgets.QApplication(sys.argv)

try:
    w = GethConnector()
    s = system()
    log = into()
except Exception as e:
    print("Фатальная ошибка при иницализации приложения:\n" +  str(e) + "\nПовторите позднее!")

try:
    sys.exit(app.exec_())
except Exception as e:
    print("Фатальная ошибка при работе приложения:\n" +  str(e) + "\nПовторите позднее!")