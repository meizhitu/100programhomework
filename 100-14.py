__author__ = 'rui'
#coding=utf-8

#计算个人所得税及年终奖
#学习一下gtk
import sys
import pygtk

pygtk.require("2.0")
import gtk
import gtk.glade

#个人部分
insuranceMax = 15669;#社保封顶数
fundMax = 15669;#公积金封顶数
pension = 8;#社保%
medicare = 2;#医疗保险%+3元
unemploymentInsurance = 0.2;#失业保险%（农村户口没有）
fund = 12;#公积金%
threshold = 3500;#个税起征点


class TaxGtk:
    def __init__(self):
        #个税起点
        self.Threshold = 3500
        self.gladeFile = r'res/tax.glade'
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladeFile)
        self.mainWindow = self.builder.get_object('taxWindow')
        self.etIncome = self.builder.get_object('etIncome')
        self.lbResult = self.builder.get_object('lbResult')
        self.checkInsurance = self.builder.get_object('checkbuttonInsurance')
        self.builder.connect_signals(self)
        if self.mainWindow:
            self.mainWindow.connect('destroy', gtk.main_quit)
            self.mainWindow.show_all()

    def getTax(self, num):#计算个人所得税
        if num < 0:
            tax = 0
        elif num < 1500:
            tax = num * 0.03
        elif num < 4500:
            tax = num * 0.1 - 105
        elif num < 9000:
            tax = num * 0.2 - 555
        elif num < 35000:
            tax = num * 0.25 - 1005
        elif num < 55000:
            tax = num * 0.3 - 2755
        elif num < 80000:
            tax = num * 0.35 - 5505
        else:
            tax = num * 0.45 - 13505
        return tax

    def getYearTaxRate(self, num):#计算个人所得税
        if num < 0:
            tax = [0, 0]
        elif num < 1500:
            tax = [0.03, 0]
        elif num < 4500:
            tax = [0.1, 105]
        elif num < 9000:
            tax = [0.2, 555]
        elif num < 35000:
            tax = [0.25, 1005]
        elif num < 55000:
            tax = [0.3, 2755]
        elif num < 80000:
            tax = [0.35, 5505]
        else:
            tax = [0.45, 13505]
        return tax

    def insuranceBase(self, num):#计算四险一金基数
        if num >= insuranceMax:
            return insuranceMax
        else:
            return num

    def calcYearBonusTax(self, num):
        taxrate = self.getYearTaxRate(num / 12)
        return num * taxrate[0] - taxrate[1]


    def calcInsurance(self, num):#计算个人四险一金缴费总额
        return self.insuranceBase(num) * (pension + medicare + unemploymentInsurance + fund) / 100 + 3

    def on_buttonMonth_clicked(self, *args):
        income = int(self.etIncome.get_text())
        bCalcInsurance = self.checkInsurance.get_active()
        if bCalcInsurance:
            insuranceOut = self.calcInsurance(income)#计算四险一金总额
            tax = self.getTax(income - self.Threshold - insuranceOut)
            textout = "四险一金缴费基数:%.2f    个人缴费总额:%.2f\r" % (self.insuranceBase(income), insuranceOut)
            textout += "社保:%.2f\r" % ((income * pension) / 100)
            textout += "医疗保险:%.2f\r" % ((income * medicare) / 100 + 3)
            textout += "失业保险:%.2f\r" % ((income * unemploymentInsurance) / 100)
            textout += "公积金:%.2f\r" % ((income * fund) / 100)
            textout += "纳税总额:%.2f    实际获得工资:%.2f\r" % (tax, income - tax - insuranceOut)
            self.lbResult.set_text(textout)
        else:
            tax = self.getTax(income - self.Threshold)
            afterTax = income - tax
            self.lbResult.set_text("扣税：{0}，税后：{1}".format(tax, afterTax))

    def on_buttonYear_clicked(self, *args):
        income = int(self.etIncome.get_text())
        tax = self.calcYearBonusTax(income)
        self.lbResult.set_text("扣税：%.2f，税后：%.2f" % (tax, income - tax))


if __name__ == "__main__":
    tax = TaxGtk()
    gtk.main()