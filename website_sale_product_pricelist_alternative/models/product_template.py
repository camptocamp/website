# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_combination_info(
        self,
        combination=False,
        product_id=False,
        add_qty=1,
        pricelist=False,
        parent_combination=False,
        only_template=False,
    ):
        if (
            pricelist
            and pricelist.discount_policy == "with_discount"
            and self.env.context.get("website_id")
        ):
            # Compute original price
            pricelist = pricelist.with_context(skip_alternative_pricelist=True)
            combination_info = super(ProductTemplate, self)._get_combination_info(
                combination,
                product_id,
                add_qty,
                pricelist,
                parent_combination,
                only_template,
            )
            combination_info["list_price"] = combination_info["price"]
            # Compute alternative price
            pricelist = pricelist.with_context(skip_alternative_pricelist=False)
            product = self.env["product.product"].browse(combination_info["product_id"])
            combination_info["price"] = pricelist._get_product_price(
                product, quantity=self.env.context.get("quantity", add_qty)
            )
            combination_info["has_discounted_price"] = (
                combination_info["price"] < combination_info["list_price"]
            )
            return combination_info
        return super()._get_combination_info(
            combination,
            product_id,
            add_qty,
            pricelist,
            parent_combination,
            only_template,
        )
