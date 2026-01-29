import requests
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class IndiaMartLead(models.Model):
    _inherit = "crm.lead"

    indiamart_query_id = fields.Char(string="IndiaMART Query ID", copy=False)
    tradeindia_query_id = fields.Char(string="Trade India Query ID", copy=False)

    #     params for indiamart:
    #         "usrid": "4004980",
    #         "profile_id": "5479707",
    #         "key": "mRy1Grhk4nfATveq4HaJ7l2JpVvEnDk="
    #         "url": "https://mapi.indiamart.com/wservce/crm/crmListing/v2/"
    #     }

    #     params for trademart:
    #         "usrid": "4004980",
    #         "profile_id": "5479707",
    #         "key": "4a27cfaed29e57212df3a2a8fd0cbf9b"
    #         "url": "https://www.tradeindia.com/utils/my_inquiry.html"
    #     }

class ApiConfig(models.Model):
    _name = "indiamart.config.settings"
    _inherit = "res.config.settings"

    name = fields.Char(string="Name")
    user_id = fields.Char(string="IndiaMART User ID")
    profile_id = fields.Char(string="IndiaMART Profile ID")
    glusr_crm_key = fields.Char(string="IndiaMART API Key")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")   
    base_url = fields.Char(string="IndiaMART Base URL")
    # "https://mapi.indiamart.com/wservce/crm/crmListing/v2/"
    cron_start_date = fields.Datetime(string="Cron Start Date")
    cron_end_date = fields.Datetime(string="Cron End Date")

    def fetch_indiamart_leads(self):
        self.ensure_one()

        if not self.glusr_crm_key or not self.start_date or not self.end_date:
            raise UserError(_("Please fill API Key, Start Date and End Date."))

        start_date_fmt = self.start_date.strftime("%d-%b-%Y")
        end_date_fmt = self.end_date.strftime("%d-%b-%Y")

        base_url = self.base_url

        url = (
            f"{base_url}"
            f"?glusr_crm_key={self.glusr_crm_key}"
            f"&start_time={start_date_fmt}"
            f"&end_time={end_date_fmt}"
        )

        _logger.info("IndiaMART Request URL: %s", url)

        response = requests.get(url, timeout=25)

        if response.status_code != 200:
            raise UserError(_("IndiaMART API failed with HTTP %s") % response.status_code)

        data = response.json()

        leads = data.get("RESPONSE", [])
        if not leads:
            raise UserError(_("No leads found from IndiaMART"))

        Lead = self.env["crm.lead"]
        Partner = self.env["res.partner"]
        State = self.env["res.country.state"]

        created_count = 0

        for item in leads:
            query_id = item.get("UNIQUE_QUERY_ID")

            # Avoid duplicates
            if Lead.search([("indiamart_query_id", "=", query_id)], limit=1):
                continue

            # Find / Create Partner
            partner = None
            if item.get("SENDER_MOBILE"):
                partner = Partner.search(
                    [("mobile", "=", item.get("SENDER_MOBILE"))], limit=1)

            if not partner:
                partner = Partner.create({
                    "name": item.get("SENDER_NAME") or "IndiaMART Contact",
                    "mobile": item.get("SENDER_MOBILE"),
                    "phone": item.get("SENDER_PHONE"),
                    "email": item.get("SENDER_EMAIL"),
                    "street": item.get("SENDER_ADDRESS"),
                    "city": item.get("SENDER_CITY"),
                    "zip": item.get("SENDER_PINCODE"),
                    "company_name": item.get("SENDER_COMPANY"),})

            # Find State
            state_id = False
            if item.get("SENDER_STATE"):
                state = State.search(
                    [("name", "ilike", item.get("SENDER_STATE"))], limit=1)
                state_id = state.id if state else False

            # Create CRM Lead
            Lead.create({
                "name": item.get("SUBJECT") or "IndiaMART Inquiry",
                "partner_id": partner.id,
                "partner_name": item.get("SENDER_COMPANY"),
                "mobile": item.get("SENDER_MOBILE"),
                "phone": item.get("SENDER_PHONE"),
                "email_from": item.get("SENDER_EMAIL"),
                "street": item.get("SENDER_ADDRESS"),
                "city": item.get("SENDER_CITY"),
                "state_id": state_id,
                "zip": item.get("SENDER_PINCODE"),
                "description": item.get("QUERY_MESSAGE"),
                "indiamart_query_id": query_id,
            })

            created_count += 1

        return {
            "effect": {
                "type": "rainbow_man",
                "message": _(f"{created_count} IndiaMART leads imported successfully!"),}
        }

class ApiConfigTrade(models.Model):
    _name = "tradeindia.config.settings"
    _inherit = "res.config.settings"

    name = fields.Char(string="Name")
    ti_user_id = fields.Char(string="Trade India User ID")
    ti_profile_id = fields.Char(string="Trade India Profile ID")
    ti_crm_key = fields.Char(string="Trade India API Key")
    ti_start_date = fields.Date(string="Start Date")
    ti_end_date = fields.Date(string="End Date") 
    ti_limit = fields.Integer(string="Limit") 
    ti_page_no = fields.Integer(string="Page No.") 
    ti_base_url = fields.Char(string="Trade India Base URL")
    ti_cron_start_date = fields.Datetime(string="Cron Start Date")
    ti_cron_end_date = fields.Datetime(string="Cron End Date")

    def fetch_tradeindia_leads(self):
        self.ensure_one()

        if not self.ti_crm_key or not self.ti_start_date or not self.ti_end_date:
            raise UserError(_("Please fill API Key, Start Date and End Date."))

        ti_start_date_fmt = self.ti_start_date.strftime("%Y-%m-%d")
        ti_end_date_fmt = self.ti_end_date.strftime("%Y-%m-%d")

        ti_base_url = self.ti_base_url
        # https://www.tradeindia.com/utils/my_inquiry.html
        limit = self.ti_limit or 10
        page_no = self.ti_page_no or 1

        ti_url = (
            f"{ti_base_url}"
            f"?userid={self.ti_user_id}"
            f"&profile_id={self.ti_profile_id}"
            f"&key={self.ti_crm_key}"
            f"&from_date={ti_start_date_fmt}"
            f"&to_date={ti_end_date_fmt}"
            f"&limit={limit}"
            f"&page_no={page_no}"
        )

        _logger.info("TradeIndia Request URL: %s", ti_url)

        response = requests.get(ti_url, timeout=30)

        if response.status_code != 200:
            raise UserError(_("TradeIndia API failed with HTTP %s") % response.status_code)

        raw_text = response.text.strip()
        _logger.info("TradeIndia Raw Response: %s", raw_text[:500])

        # Maintenance / plain-text response
        if "maintenance" in raw_text.lower():
            raise UserError(_(
                "TradeIndia service is currently under maintenance. "
                "Please try again later."
            ))

        # HTML response
        if raw_text.startswith("<"):
            raise UserError(_(
                "TradeIndia returned HTML instead of JSON. "
                "Please check API credentials or try again later."
            ))

        # Parse JSON
        try:
            import json
            data = json.loads(raw_text)
        except Exception:
            raise UserError(_("TradeIndia returned invalid JSON response"))

        # Extract leads
        if isinstance(data, dict):
            leads = data.get("RESPONSE") or data.get("response") or []
        elif isinstance(data, list):
            leads = data
        else:
            raise UserError(_("TradeIndia returned unsupported response format"))

        if not leads:
            raise UserError(_("No leads found from TradeIndia"))

        Lead = self.env["crm.lead"]
        Partner = self.env["res.partner"]
        State = self.env["res.country.state"]

        created_count = 0

        for item in leads:
            query_id = item.get("inq_id")
            if not query_id:
                continue

            if Lead.search([("tradeindia_query_id", "=", query_id)], limit=1):
                continue

            mobile = item.get("sender_mobile")
            partner = Partner.search([("mobile", "=", mobile)], limit=1) if mobile else None

            if not partner:
                partner = Partner.create({
                    "name": item.get("sender_name") or "TradeIndia Contact",
                    "mobile": mobile,
                    "phone": item.get("sender_phone"),
                    "email": item.get("sender_email"),
                    "street": item.get("sender_address"),
                    "city": item.get("sender_city"),
                    "zip": item.get("sender_pincode"),
                    "company_name": item.get("sender_company"),
                })

            state_id = False
            if item.get("sender_state"):
                state = State.search([("name", "ilike", item.get("sender_state"))], limit=1)
                state_id = state.id if state else False

            Lead.create({
                "name": item.get("subject") or "TradeIndia Inquiry",
                "partner_id": partner.id,
                "partner_name": item.get("sender_company"),
                "mobile": mobile,
                "phone": item.get("sender_phone"),
                "email_from": item.get("sender_email"),
                "street": item.get("sender_address"),
                "city": item.get("sender_city"),
                "state_id": state_id,
                "zip": item.get("sender_pincode"),
                "description": item.get("message"),
                "tradeindia_query_id": query_id,
            })

            created_count += 1

        return {
            "effect": {
                "type": "rainbow_man",
                "message": _(f"{created_count} TradeIndia leads imported successfully!"),}
        }

