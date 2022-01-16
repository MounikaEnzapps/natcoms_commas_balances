from odoo import fields, models,api
from odoo.exceptions import UserError

from uuid import uuid4
import qrcode
import base64
import logging
from odoo.addons import decimal_precision as dp

from lxml import etree

from odoo import fields, models
import requests
import json
from datetime import datetime,date
import convert_numbers


class AccountMove(models.Model):
    _inherit = 'account.move'
    _order = "invoice_nat_times desc"


    net_amount_jan = fields.Float(compute='_net_amount_jan',digits=dp.get_precision('Product Unit of Measure'))
    discount_comma = fields.Float(compute='_compute_discount_comma',digits=dp.get_precision('Product Unit of Measure'))
    advance_comma = fields.Float(compute='_compute_advance_comma',digits=dp.get_precision('Product Unit of Measure'))
    net_amount_jan_arabic = fields.Float(compute='_net_amount_jan_ar',digits=dp.get_precision('Product Unit of Measure'))
    vat_amount_comma = fields.Float(compute='_vat_amount_comma',digits=dp.get_precision('Product Unit of Measure'))
    net_amount_with_comma = fields.Float(compute='_net_amount_with_vat_comma',digits=dp.get_precision('Product Unit of Measure'))
    total_amount_comma = fields.Float(compute='_compute_total_amount_comma',digits=dp.get_precision('Product Unit of Measure'))


    def amount_untaxed_convert(self):
        value = '%.2f' % self.amount_untaxed
        before, after = str(value).split('.')
        before_int = int(before)
        after_int = int(after)

        before_ar = convert_numbers.english_to_arabic(before_int)
        after_ar = convert_numbers.english_to_arabic(after_int)
        # ar_total_tax_amount = before_ar + '.' + after_ar
        list_mou = ''
        for l in after:
            print(l,'dfvdfgdf')
            if l == '0':
                list_mou+="٠"
            if l == '1':
                list_mou+="١"
            if l == '2':
                list_mou+="٢"
            if l == '3':
                list_mou+="٣"
            if l == '4':
                list_mou+="٤"
            if l == '5':
                list_mou+="٥"
            if l == '6':
               list_mou+="٦"
            if l == '7':
               list_mou+="٧"
            if l == '8':
                list_mou+="٨"
            if l == '9':
               list_mou+="٩"

        # after_int = int(after)
        after_ar = list_mou


        # arabic_no = list('۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹')
        # list("٠", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩")


        # $string = str_replace($persianDecimal, $newNumbers, $string);
        # $string = str_replace($arabicDecimal, $newNumbers, $string);
        # $string = str_replace($arabic, $newNumbers, $string);
        # return str_replace($persian, $newNumbers, $string);


        return before_ar + '.' + after_ar


    def _compute_discount_comma(self):
        for each in self:
            if each.discount_value:
                each.discount_comma = float(each.discount_value)
            else:
                each.discount_comma = float(0)
    def _compute_advance_comma(self):
        for each in self:
            if each.advance:
                each.advance_comma = float(each.advance)
            else:
                each.advance_comma = float(0)
    def _vat_amount_comma(self):
        for each in self:
            if each.state == 'posted':
                tax_amount = each.amount_untaxed - float(each.advance) - float(each.discount_value)
                each.vat_amount_comma = tax_amount * 0.15
            else:
                each.vat_amount_comma = 0
    def _net_amount_with_vat_comma(self):
        for each in self:
            if each.state == 'posted':
                tax_amount =  each.amount_untaxed - float(each.advance) - float(each.discount_value)
                value = tax_amount * 0.15
                each.net_amount_with_comma = tax_amount+value
            else:
                each.net_amount_with_comma = 0





    def _net_amount_jan(self):
        for each in self:
            if each.state == 'posted':
               each.net_amount_jan = float(each.amount_untaxed - float(each.advance) - float(each.discount_value))
            else:
                each.net_amount_jan = 0
         # return self.net_amount_jan


    def _compute_total_amount_comma(self):
        for each in self:
            if each.state == 'posted':
               net_amount = float(each.amount_untaxed)
               before, after = str(net_amount).split('.')
               before_int = int(before)
               after_int = int(after)
               before_ar = convert_numbers.english_to_arabic(before_int)
               after_ar = convert_numbers.english_to_arabic(after_int)
               each.total_amount_comma = before_ar + '.' + after_ar
               # return before_ar + '.' + after_ar

               # each.net_amount_jan_arabic = convert_numbers.english_to_arabic(int(net_amount))
            else:
                # each.net_amount_jan_arabic = convert_numbers.english_to_arabic(int(0))
                before_int = int(0)
                after_int = int(00)
                before_ar = convert_numbers.english_to_arabic(before_int)
                after_ar = convert_numbers.english_to_arabic(after_int)
                each.net_amount_jan_arabic = before_ar + '.' + after_ar


    def _net_amount_jan_ar(self):
        for each in self:
            if each.state == 'posted':
               net_amount = float(each.amount_untaxed - float(each.advance) - float(each.discount_value))

               before, after = str(net_amount).split('.')
               before_int = int(before)
               after_int = int(after)
               before_ar = convert_numbers.english_to_arabic(before_int)
               after_ar = convert_numbers.english_to_arabic(after_int)
               each.net_amount_jan_arabic = before_ar + '.' + after_ar
               # return before_ar + '.' + after_ar

               # each.net_amount_jan_arabic = convert_numbers.english_to_arabic(int(net_amount))
            else:
                # each.net_amount_jan_arabic = convert_numbers.english_to_arabic(int(0))
                before_int = int(0)
                after_int = int(00)
                before_ar = convert_numbers.english_to_arabic(before_int)
                after_ar = convert_numbers.english_to_arabic(after_int)
                each.net_amount_jan_arabic = before_ar + '.' + after_ar

         # return self.net_amount_jan



    def amount_tax_per(self):
        tax_amount =  self.amount_untaxed - float(self.advance) - float(self.discount_value)
        value = tax_amount * 0.15
        return value
    def amount_net_amount(self):
        net_amount = self.amount_untaxed - float(self.advance) - float(self.discount_value)
        net_amount = '%.2f' % net_amount
        list_mou = ''
        before, after = str(net_amount).split('.')
        before_int = int(before)
        after_int = int(after)
        before_ar = convert_numbers.english_to_arabic(before_int)
        for l in after:
            print(l, 'dfvdfgdf')
            if l == '0':
                list_mou += "٠"
            if l == '1':
                list_mou += "١"
            if l == '2':
                list_mou += "٢"
            if l == '3':
                list_mou += "٣"
            if l == '4':
                list_mou += "٤"
            if l == '5':
                list_mou += "٥"
            if l == '6':
                list_mou += "٦"
            if l == '7':
                list_mou += "٧"
            if l == '8':
                list_mou += "٨"
            if l == '9':
                list_mou += "٩"

        # after_int = int(after)
        after_ar = list_mou

        # return convert_numbers.english_to_arabic(int(net_amount))
        return before_ar + '.' + after_ar

    def amount_tax_per_arabic(self):
        m= self.amount_untaxed - float(self.advance) - float(self.discount_value)
        value = m * 0.15
        value = '%.2f' % value
        before, after = str(value).split('.')
        before_int = int(before)
        after_int = int(after)
        before_ar = convert_numbers.english_to_arabic(before_int)
        after_ar = convert_numbers.english_to_arabic(after_int)
        list_mou = ''
        for l in after:
            print(l, 'dfvdfgdf')
            if l == '0':
                list_mou += "٠"
            if l == '1':
                list_mou += "١"
            if l == '2':
                list_mou += "٢"
            if l == '3':
                list_mou += "٣"
            if l == '4':
                list_mou += "٤"
            if l == '5':
                list_mou += "٥"
            if l == '6':
                list_mou += "٦"
            if l == '7':
                list_mou += "٧"
            if l == '8':
                list_mou += "٨"
            if l == '9':
                list_mou += "٩"
        ar_total_tax_amount = before_ar + '.' + after_ar
        return before_ar + '.' + list_mou

    def net_amount_with_vat(self):
        tax_amount =  self.amount_untaxed - float(self.advance) - float(self.discount_value)
        value = tax_amount * 0.15
        return tax_amount+value
    def ar_net_amount_with_vat(self):
        tax_amount = self.amount_untaxed - float(self.advance) - float(self.discount_value)
        value = tax_amount * 0.15
        with_vat = tax_amount + value
        with_vat = '%.2f' % with_vat
        before, after = str(with_vat).split('.')
        before_int = int(before)
        after_int = int(after)
        before_ar = convert_numbers.english_to_arabic(before_int)
        list_mou = ''
        for l in after:
            print(l, 'dfvdfgdf')
            if l == '0':
                list_mou += "٠"
            if l == '1':
                list_mou += "١"
            if l == '2':
                list_mou += "٢"
            if l == '3':
                list_mou += "٣"
            if l == '4':
                list_mou += "٤"
            if l == '5':
                list_mou += "٥"
            if l == '6':
                list_mou += "٦"
            if l == '7':
                list_mou += "٧"
            if l == '8':
                list_mou += "٨"
            if l == '9':
                list_mou += "٩"
        # return convert_numbers.english_to_arabic(int(with_vat))
        return before_ar + '.' + list_mou

