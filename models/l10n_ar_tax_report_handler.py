# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from odoo import models, _

_logger = logging.getLogger(__name__)


class AccountGenericTaxReport(models.AbstractModel):
    """Extend account.generic.tax.report for Argentinean localization.
    
    This extends the generic tax report functionality for Argentinean
    localization. In Odoo 17, this is provided by the base l10n_ar_reports
    module, but in Odoo 15 we need to extend it directly.
    """
    _inherit = 'account.generic.tax.report'

    def _get_reports_buttons(self, options):
        """Add IVA Simple export button for Argentinean companies."""
        _logger.info("l10n_ar_reports_simple: _get_reports_buttons called for model %s", self._name)
        buttons = super()._get_reports_buttons(options)
        # Check company country (most reliable method)
        try:
            company = self.env.company
            company_country = company.account_fiscal_country_id.code if company.account_fiscal_country_id else None
            _logger.info("l10n_ar_reports_simple: Company=%s, Country code=%s", company.name, company_country)
            if company_country == 'AR':
                buttons.append({
                    'name': _('Reporte de IVA Simple (ZIP)'),
                    'sequence': 31,
                    'action': 'vat_simple_export_files_to_zip',
                    'file_export_type': _('ZIP')
                })
                _logger.info("l10n_ar_reports_simple: Added IVA Simple button. Total buttons: %d", len(buttons))
            else:
                _logger.info("l10n_ar_reports_simple: Company country is '%s' (not AR), button not added", company_country)
        except Exception as e:
            _logger.error("l10n_ar_reports_simple: Error in _get_reports_buttons: %s", str(e), exc_info=True)
        return buttons


