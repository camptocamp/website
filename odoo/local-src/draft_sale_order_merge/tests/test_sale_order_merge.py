# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA (Nicolas Bessi)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestSalesOrderMerge(TransactionCase):
    def make_so_lines(self):
        self.assertTrue(self.partner, 'partner_id not set')
        products = {
            'prod_order': self.env.ref('product.product_order_01'),
            'prod_del': self.env.ref('product.product_delivery_01'),
            'serv_order': self.env.ref('product.service_order_01'),
            'serv_del': self.env.ref('product.service_delivery'),
        }
        lines = [(0, 0,
                 {'name': p.name,
                  'product_id': p.id,
                  'product_uom_qty': 2,
                  'product_uom': p.uom_id.id,
                  'price_unit': p.list_price}
                  ) for (_, p) in products.iteritems()]
        return lines

    def setUp(self):
        """Test The merge of Sales Order"""
        super(TestSalesOrderMerge, self).setUp()
        self.partner = self.env.ref('base.res_partner_address_3')

        self.confirmed_so = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'partner_invoice_id': self.partner.id,
            'partner_shipping_id': self.partner.id,
            'order_line': self.make_so_lines(),
            'pricelist_id': self.env.ref('product.list0').id,

        })
        self.confirmed_so.force_quotation_send()
        self.assertTrue(self.confirmed_so.state == 'sent',
                        'Sale: state after sending is wrong')
        self.confirmed_so.action_confirm()

        self.draft_so_1 = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'partner_invoice_id': self.partner.id,
            'partner_shipping_id': self.partner.id,
            'order_line': self.make_so_lines(),
            'pricelist_id': self.env.ref('product.list0').id,
        })

        self.draft_so_2 = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'partner_invoice_id': self.partner.id,
            'partner_shipping_id': self.partner.id,
            'order_line': self.make_so_lines(),
            'pricelist_id': self.env.ref('product.list0').id,
        })

        self.target_so = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'partner_invoice_id': self.partner.id,
            'partner_shipping_id': self.partner.id,
            'order_line': self.make_so_lines(),
            'pricelist_id': self.env.ref('product.list0').id,
        })

        self.non_candidate_so = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_address_5').id,
            'partner_invoice_id': self.env.ref(
                'base.res_partner_address_5').id,
            'partner_shipping_id': self.env.ref(
                'base.res_partner_address_5').id,
            'order_line': self.make_so_lines(),
            'pricelist_id': self.env.ref('product.list0').id,
        })

        self.valid_candidates = self.env['sale.order'].browse(
            [self.draft_so_1.id, self.draft_so_2.id])

    def test_candidate_validity(self):
        """ Dummy test to verify that tests run """
        self.assertEqual(
            self.valid_candidates,
            self.target_so.merge_candidates,
            "Merge candidates are invalid"
        )

    def test_wizard_initialisation(self):
        """Test wizard default values"""
        wizard_model = self.env['draft_sale_order_merger'].with_context(
            active_id=self.target_so.id
        )
        wizard = wizard_model.create({})
        self.assertEquals(
            self.target_so,
            wizard.target_so,
            'Target Sales order does not match with context'
        )

        self.assertEqual(
            self.valid_candidates,
            wizard.merge_candidates,
            'Proposed sources Sales orders are invalid'
        )

    def test_wizard_merge(self):
        """Test merge of Sales orders """
        wizard_model = self.env['draft_sale_order_merger'].with_context(
            active_id=self.target_so.id
        )
        wizard = wizard_model.create({})
        numbers_of_lines = (len(wizard.merge_candidates.mapped('order_line')) +
                            len(wizard.target_so.order_line))
        wizard.merge_sale_orders()

        self.assertFalse(any(wizard.merge_candidates.mapped('active')),
                         'Some sources Sales order where not deactivated')
        self.assertEquals(numbers_of_lines,
                          len(wizard.target_so.order_line),
                          "Wrong number of Sales lines in target")
        self.assertEquals(wizard.target_so.amount_total, 3720.00,
                          'Target Sales order amount is invalid')
