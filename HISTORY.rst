.. :changelog:

.. Template:

.. 0.0.1 (2016-05-09)
.. ++++++++++++++++++

.. **Features and Improvements**

.. **Bugfixes**

.. **Build**

.. **Documentation**

Release History
---------------

latest (unreleased)
+++++++++++++++++++

**Features and Improvements**

* Install web_m2x_options and configured to remove quick create
* Install hr_expense_usability

**Bugfixes**

* [fix] empty space before blogpost title BCS-10


**Build**

**Documentation**


10.5.1 (2017-09-13)
+++++++++++++++++++

**Features and Improvements**

**Bugfixes**

* fixes 404 on contact form https://jira.camptocamp.com/browse/BIZ-492

**Build**

**Documentation**


10.5.0 (2017-09-06)
+++++++++++++++++++

**Features and Improvements**

* Install ribbon
* Add dj_tool
* Install e-shop (website_sale) & hide menuitems for non-authenticated users

**Bugfixes**

**Build**

* Update odoo-template to 10.0-2.3.0
* Remove old pending-merge

**Documentation**


10.4.0 (2017-06-15)
+++++++++++++++++++

**Features and Improvements**

* Add the custom sale_order_merge addon.(odoo incident 4075)

10.3.7 (2017-06-12)
+++++++++++++++++++

**Features and Improvements**

* Remove registration from event web page

10.3.6 (2017-05-11)
+++++++++++++++++++

**Features and Improvements**

* Add SO line description to manual delivery lines
* Print stock operations instead of stock moves in delivery slip

10.3.5 (2017-04-13)
+++++++++++++++++++

**Features and Improvements**
* Add product name to manual delivery lines

10.3.4 (2017-03-22)
+++++++++++++++++++

**Bugfixes**
* Fix description in invoice report

10.3.3 (2017-03-09)
+++++++++++++++++++

**Bugfixes**
* Fix in invoice, sale, po, out reports
* Add lang in partner contact form
* remove warning on sale order
* Correct multiple picking for manual delivery
* Fix website languages
* correct "delivered quantity" on OUT report

10.3.2 (2017-03-02)
+++++++++++++++++++

**Bugfixes**
* Fix keep normal picking assign if not manual delivery


10.3.1 (2017-02-21)
+++++++++++++++++++

**Features and Improvements**

* Changes in reports

**Bugfixes**

* Fixes in sale_manual_delivery:
  * Wizard not displayed in the SO
  * 1 picking is now created per manual delivery


10.3.0 (2017-02-16)
+++++++++++++++++++

**Features and Improvements**

* Reports corrections:
  * activate settings (proforma, discount, uom, group_sale_layout)
  * update lang formats (en,fr,de)
  * Addresses in 'Quotation / Order' & 'Quotation'
  * Lines in 'Quotation'
  * Addresses in Invoices
  * Information labels in invoice
* Configure BVR details for main bank
* Add module "sale_manual_delivery"

**Bugfixes**

* Re-install all modules to correct missing ones from 10.0.0


10.2.1 (2017-02-09)
+++++++++++++++++++

**Features and Improvements**

* Add decimal precision of 6 on product volume
* Add "Latest posts" snippet module


10.2.0 (2017-02-08)
+++++++++++++++++++

**Features and Improvements**

* Add Graphene theme (bought from Odoo SA)


10.1.0 (2017-01-24)
+++++++++++++++++++

**Features and Improvements**

* Add l10n_ch_bank
* Add l10n_ch_zip
* Add  l10n_ch_states
* Port sales_product_set
* Port sales_product_set_layout
* Add specific_report:
  * Quotation / Sale Order.  Note: the order of columns has changed
  * Invoice.  Note: There was two fields referring to the same place "Reference /  Description". This is now on the field "Description".
  * Delivery.  Note: Some changes in the headers
  * Purchase Order.  Note: there is not anymore the "validate by:" field
  * Mrp / Quotation.  Note: 'Lot id' label is diplayed only if there is one.
  * Translations
* Add specific_fct:
  * Add total to inventory valuation + field in pivot view

**Bugfixes**

* Improves web performance thanks to a correction in attachment_s3


10.0.0 (2016-12-22)
+++++++++++++++++++

Initial setup.

* Install generic addons
* Base setup of the company
* Activate multicurrency
* Load banks
* Load accounts
* Load journals
* Setup currency rate updates
* Load users and change admin password
* Install cloud platform
