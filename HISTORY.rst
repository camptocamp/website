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

Unreleased
++++++++++

**Features and Improvements**

**Bugfixes**

**Build**

**Documentation**


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
