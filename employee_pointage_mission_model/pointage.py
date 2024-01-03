from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar
import locale
import math


class hr_rapport_pointage(models.Model):
    _name = "hr.rapport.pointage"
    _description = "Rapport de Pointage"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    READONLY_STATES = {
        "working": [("readonly", True)],
        "valide": [("readonly", True)],
        "compute": [("readonly", True)],
        "done": [("readonly", True)],
        "cancel": [("readonly", True)],
    }

    def _get_period_default(self):
        domain = [("id", "=", "-1")]
        year = date.today().year
        period_ids = []
        for mois_id in self.env["account.month.period"].search(
            [
                ("date_stop", "<=", str(year) + "-12-31"),
                ("date_start", ">=", str(year) + "-01-01"),
            ]
        ):
            period_ids.append(mois_id.id)
        if period_ids:
            domain = [("id", "in", period_ids)]
        return domain

    @api.depends("rapport_lines.h_travailler")
    def _compute_total_h(self):
        for rapport in self:
            rapport.total_h = sum(
                float(line.h_travailler) for line in rapport.rapport_lines
            )

    @api.depends("rapport_lines.h_bonus")
    def _compute_total_h_bonus(self):
        for rapport in self:
            rapport.total_h_bonus = sum(
                float(line.h_bonus) for line in rapport.rapport_lines
            )

    @api.depends("rapport_lines.h_sup")
    def _compute_total_h_sup(self):
        for rapport in self:
            rapport.total_h_sup = sum(
                float(line.h_sup) for line in rapport.rapport_lines
            )

    @api.depends("rapport_lines.h_travailler_v")
    def _compute_total_h_v(self):
        for rapport in self:
            rapport.total_h_v = sum(
                float(line.h_travailler_v) for line in rapport.rapport_lines
            )

    @api.depends("rapport_lines.j_travaille")
    def _compute_total_j(self):
        for rapport in self:
            rapport.total_j = sum(
                float(line.j_travaille) for line in rapport.rapport_lines
            )

    @api.depends("rapport_lines.j_travaille_v","rapport_lines.state")
    def _compute_total_j_v(self):
        for rapport in self:
            rapport.total_j_v = sum(
                float(line.j_travaille_v) for line in rapport.rapport_lines.filtered(
                    lambda ln: ln.day_type in ("1","3") and float(ln.h_travailler) > 0
                )
            )

    @api.depends("rapport_lines.j_travaille", "rapport_lines.day_type")
    def _compute_sundays(self):
        for rapport in self:
            rapport.count_nbr_dim_days = sum(
                float(line.j_travaille)
                for line in rapport.rapport_lines.filtered(
                    lambda ln: ln.day_type == "2" and float(ln.h_travailler) > 0
                )
            )

    @api.depends("rapport_lines.day_type")
    def _compute_jour_ferie(self):
        for rapport in self:
            rapport.count_nbr_ferier_days = len(
                rapport.rapport_lines.filtered(lambda ln: ln.day_type == "3" and ln.day > rapport.employee_id.contract_id.date_start)
            )

    @api.depends(
        "rapport_lines.j_travaille",
        "rapport_lines.day_type",
        "rapport_lines.h_travailler_v",
    )
    def _compute_sundays_valide(self):
        for rapport in self:
            rapport.count_nbr_dim_days_v = sum(
                float(line.j_travaille_v)
                for line in rapport.rapport_lines.filtered(
                    lambda ln: ln.day_type == "2" and float(ln.h_travailler_v) > 0
                )
            )

    @api.depends(
        "rapport_lines.j_travaille",
        "rapport_lines.day_type",
        "rapport_lines.h_travailler_v",
        "rapport_lines.state",
    )
    def _compute_jour_ferier_valide(self):
        for rapport in self:
            rapport.count_nbr_ferier_days_v = len(rapport.rapport_lines.filtered(
                    lambda ln: ln.day_type == "3" and float(ln.h_travailler_v) > 0 and ln.day > rapport.employee_id.contract_id.date_start
                )
            )

    @api.depends("rapport_lines.j_travaille","rapport_lines.h_travailler_v","rapport_lines.day_type")
    def _compute_days_absence(self):
        for rapport in self:
            rapport.count_nbr_absense_days = sum(
                float(line.j_travaille)
                for line in rapport.rapport_lines.filtered(
                    lambda ln: ln.day_type == "5" or (ln.day_type == "1" and float(ln.h_travailler_v) == 0)
                )
            )

    @api.depends("holiday_ids.duree_jours")
    def _compute_total_holidays(self):
        for rapport in self:
            rapport.count_nbr_holiday_days = sum(
                float(line.duree_jours) for line in rapport.holiday_ids
            )

    @api.depends("holiday_ids.nbr_jour_compenser","holiday_ids.state")
    def _compute_valide_holidays(self):
        for rapport in self:
            rapport.count_nbr_holiday_days_v = sum(
                float(line.nbr_jour_compenser) for line in rapport.holiday_ids
            )

    def _compute_holidays_liste(self):
        date_start = self.rapport_lines[0].day
        date_stop = self.rapport_lines[len(self.rapport_lines) - 1].day

        for employee_id in self.employee_id:
            
            self.holiday_ids = self.env["hr.holidays"].search(
                [
                    ("employee_id", "=", employee_id.id),
                    ("state", "!=", "draft"),
                    "|",
                    "|",
                    "&",
                    ("date_start", ">=", date_start),
                    ("date_start", "<=", date_stop),
                    "&",
                    ("date_end", ">=", date_start),
                    ("date_end", "<=", date_stop),
                    "&",
                    ("date_select_half_perso", ">=", date_start),
                    ("date_select_half_perso", "<=", date_stop),
                ]
            )

    def _compute_transferts_liste(self):
        date_start = self.rapport_lines[0].day
        date_stop = self.rapport_lines[len(self.rapport_lines) - 1].day

        self.transfert_ids = self.env["hr.employee.transfert"].search(
            [
                ("employee_id", "=", self.employee_id.id),
                "|",
                "&",
                ("date_transfert", ">=", date_start),
                ("date_transfert", "<=", date_stop),
                "&",
                ("date_arriver", ">=", date_start),
                ("date_arriver", "<=", date_stop),
            ]
        )

    name = fields.Char("Référence", readonly=True)
    employee_id = fields.Many2one(
        "hr.employee", "Employée", readonly=True, ondelete="cascade"
    )
    cin = fields.Char(related="employee_id.cin", string="N° CIN", readonly=True)
    fonction = fields.Char(related="employee_id.job", string="Fonction", readonly=True)
    job_id = fields.Many2one(
        related="employee_id.job_id", string="Poste occupé", readonly=True
    )

    chantier_id = fields.Many2one(
        "fleet.vehicle.chantier", "Dernier Chantier", readonly=True, index=True
    )
    periodicite = fields.Selection(related="chantier_id.periodicite", readonly=True)
    grant_modification = fields.Boolean(
        related="chantier_id.grant_modification", readonly=True
    )

    vehicle_id = fields.Many2one("fleet.vehicle", "Dérnier Code engin", readonly=True)
    emplacement_chantier_id = fields.Many2one(
        "fleet.vehicle.chantier.emplacement",
        "Dernière Équipe",
        readonly=True,
        index=True,
    )

    period_id = fields.Many2one(
        "account.month.period",
        "Période",
        required=True,
        readonly=True,
        domain=_get_period_default,
        index=True,
    )

    # --------------------------------------------------
    total_h = fields.Float(
        "Heures Travaillées", compute="_compute_total_h", readonly=True, store=True
    )
    total_h_bonus = fields.Float(
        "Heures Bonus", compute="_compute_total_h_bonus", readonly=True, store=True
    )
    total_h_sup = fields.Float(
        "Heures Supp", compute="_compute_total_h_sup", readonly=True, store=True
    )
    total_j = fields.Float(
        "Jours Travaillés", readonly=True, compute="_compute_total_j", store=True
    )
    total_h_v = fields.Float(
        "Heures Validées", compute="_compute_total_h_v", readonly=True, store=True
    )
    total_j_v = fields.Float(
        "Jours Validés", readonly=True, compute="_compute_total_j_v", store=True
    )
    # --------------------------------------------------
    note = fields.Text("Observation", states=READONLY_STATES)

    payslip_ids = fields.One2many(
        "hr.payslip", "rapport_id", "Fiche Paie", readonly=True
    )
    holiday_ids = fields.One2many(
        "hr.holidays", "rapport_id", "Congés", compute="_compute_holidays_liste"
    )
    rapport_lines = fields.One2many(
        "hr.rapport.pointage.line", "rapport_id", string="Lignes Rapport Pointage"
    )
    transfert_ids = fields.One2many(
        "hr.employee.transfert",
        "rapport_id",
        "Transfert",
        readonly=True,
        compute="_compute_transferts_liste",
    )

    quinzaine = fields.Selection(
        [
            ("quinzaine1", "Première quinzaine"),
            ("quinzaine2", "Deuxième quinzaine"),
            ("quinzaine12", "Q1 + Q2"),
        ],
        string="Quinzaine",
    )

    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("working", "Traitement En Cours"),
            ("compute", "Rapport Calculé"),
            ("valide", "Validé"),
            ("done", "Clôturé"),
            ("cancel", "Annulé"),
        ],
        "Etat Pointage",
        default="draft",
        tracking=True,
    )
    # --------------------------------------------------
    count_nbr_holiday_days = fields.Float(
        "Jours Congés", readonly=True, compute="_compute_total_holidays"
    )
    count_nbr_ferier_days = fields.Float(
        "Jours Fériés", readonly=True, compute="_compute_jour_ferie", store=True
    )
    count_nbr_dim_days = fields.Float(
        "Dimanches", readonly=True, compute="_compute_sundays", store=True
    )
    count_nbr_absense_days = fields.Float(
        "Absences", readonly=True, compute="_compute_days_absence", store=True
    )

    count_nbr_holiday_days_v = fields.Float(
        "Jours Congés Validés", readonly=True, compute="_compute_valide_holidays"
    )
    count_holiday_days_v = fields.Float(
        "Jours Congés Validés", readonly=True
    )
    count_nbr_ferier_days_v = fields.Float(
        "Jours Fériés Travaillés",
        readonly=True,
        compute="_compute_jour_ferier_valide",
        store=True,
    )
    count_nbr_dim_days_v = fields.Float(
        "Dimanches Validés",
        readonly=True,
        compute="_compute_sundays_valide",
        store=True,
    )
    # --------------------------------------------------
    jom = fields.Float(related="period_id.jom", readonly=True)

    q1_state = fields.Selection(
        [
            ("q1_draft", "En Attente"),
            ("q1_working", "Q1 Traitement En Cours"),
            ("q1_compute", "Q1 Calculé"),
            ("q1_valide", "Q1 Validé"),
            ("q1_done", "Q1 Clôturé"),
        ],
        "Première Quinzaine",
        default="q1_draft",
    )
    q2_state = fields.Selection(
        [
            ("q2_draft", "En Attente"),
            ("q2_working", "Q2 Traitement En Cours"),
            ("q2_compute", "Q2 Calculé"),
            ("q2_valide", "Q2 Validé"),
            ("q2_done", "Q2 Clôturé"),
        ],
        "Deuxième Quinzaine",
        default="q2_draft",
    )

    type_emp = fields.Selection(
        related="employee_id.contract_id.type_emp",
        string="Type d'employé",
        required=False,
        store=True,
    )

    def _compute_message_change_chantier(self):
        self.message_change_chantier = False
        if self.employee_id.contract_id.contract_type.depends_emplacement == True:
            for rapport_line in self.rapport_lines:
                if (
                    rapport_line.chantier_id.id
                    != self.employee_id.contract_id.chantier_id.id
                    and rapport_line.chantier_id
                ):
                    self.message_change_chantier = "Attention !!! Cet employée posséde une contrat de chantier et il y a un changement de chantier détécté durant cette période."

    def _compute_message_end_existence_contract(self):
        self.message_end_existence_contract = False
        if self.employee_id.contract_id:
            if self.employee_id.contract_id.contract_type.depends_duration == True:
                end_date = datetime.now()
                start_date = self.employee_id.contract_id.date_end
                num_months = 0
                num_jours = 0
                if start_date:
                    num_months = (start_date.year - end_date.year) * 12 + (
                        start_date.month - end_date.month
                    )
                    num_jours = start_date.day - end_date.day

                if num_months > 0.0 and num_months <= 3.0 or num_jours > 0:
                    self.message_end_existence_contract = (
                        "Attention !!! Contrat de %s sera terminé dans %s mois et %s jours. Date de fin de contrat est %s"
                        % (
                            self.employee_id.name,
                            str(num_months),
                            str(num_jours),
                            start_date,
                        )
                    )
                else:
                    self.message_end_existence_contract = False
        else:
            self.message_end_existence_contract = (
                "Attention !!! Cet employé n'a pas encore de contrat"
            )

    def _compute_message_last_periode(self):
        obj = self.env["hr.payslip"]
        self.message_last_periode = False
        self.message_gap_payement = False

        if self.period_id:
            date_stop = self.period_id.date_stop - relativedelta(months=+1)
            date_start = self.period_id.date_start - relativedelta(months=+1)
            period_id = self.env["account.month.period"].search(
                [("date_stop", ">=", date_stop), ("date_start", "<=", date_start)],
                limit=1,
            )

            prev_paied_period = obj.search(
                [
                    ("employee_id", "=", self.employee_id.id),
                    ("period_id", "=", period_id.id),
                    ("quinzaine", "=", self.quinzaine),
                ]
            )
            last_period = (
                obj.search(
                    [
                        ("employee_id", "=", self.employee_id.id),
                        ("period_id", "!=", self.period_id.id),
                    ],
                    limit=1,
                    order="id desc",
                )
                if not prev_paied_period
                else prev_paied_period
            )
            if not prev_paied_period:
                self.message_gap_payement = "Un décalage de paiement est détecté"
            if last_period:
                self.message_last_periode = "Dernière période payée %s" % (
                    last_period.period_id.name
                )
            else:
                self.message_last_periode = "C'est la première période travaillée"

    message_change_chantier = fields.Char(
        "message_change_chantier", compute="_compute_message_change_chantier"
    )
    message_end_existence_contract = fields.Char(
        "message_end_existence_contract",
        compute="_compute_message_end_existence_contract",
    )
    message_last_periode = fields.Char(
        "message_last_periode", compute="_compute_message_last_periode"
    )
    message_gap_payement = fields.Char(
        "message_gap_payement", compute="_compute_message_last_periode"
    )

    @api.model
    def create(self, vals):
        res = True
        employee_id = self.env["hr.employee"].browse(vals["employee_id"])
        vals["name"] = self.env["ir.sequence"].next_by_code(
            "hr.rapport.pointage.sequence"
        )
        if not vals.get("chantier_id"):
            vals["chantier_id"] = (
                employee_id.chantier_id.id if employee_id.chantier_id else False
            )
        vals["emplacement_chantier_id"] = (
            employee_id.emplacement_chantier_id.id
            if employee_id.emplacement_chantier_id
            else False
        )
        vals["vehicle_id"] = (
            employee_id.vehicle_id.id if employee_id.vehicle_id else False
        )

        if_exist = self.env["hr.rapport.pointage"].search_count(
            [
                ("period_id", "=", vals["period_id"]),
                ("employee_id", "=", vals["employee_id"]),
                ("quinzaine", "=", vals["quinzaine"]),
            ]
        )
        if if_exist == 0:
            res = super(hr_rapport_pointage, self).create(vals)

            if res.employee_id.type_emp == "o":
                if res.quinzaine == "quinzaine1":
                    for line in self._prepare_rapport_pointage_lines(
                        res.period_id,
                        res.id,
                        vals["employee_id"],
                        res.emplacement_chantier_id.id,
                    ):
                        if line["day"].date() <= self.get_half_month_day(res.period_id):
                            self.env["hr.rapport.pointage.line"].create(line)
                elif res.quinzaine == "quinzaine2":
                    for line in self._prepare_rapport_pointage_lines(
                        res.period_id,
                        res.id,
                        vals["employee_id"],
                        res.emplacement_chantier_id.id,
                    ):
                        if line["day"].date() > self.get_half_month_day(res.period_id):
                            self.env["hr.rapport.pointage.line"].create(line)
            else:
                for line in self._prepare_rapport_pointage_lines(
                    res.period_id,
                    res.id,
                    vals["employee_id"],
                    res.emplacement_chantier_id.id,
                ):
                    self.env["hr.rapport.pointage.line"].create(line)

        return res

    def write(self, vals):
        if "state" in vals:
            for line in self.rapport_lines:
                line.write({"state": vals["state"]})
        return super().write(vals)

    def _prepare_rapport_pointage_lines(
        self, period_id, rapport_id, employee_id, emplacement_chantier_id
    ):
        nbr_days_months = self.get_range_month(period_id)
        repport_lines = []
        special_days = self.get_declaration_per_period(
            self.get_jour_ferie_per_period(
                self.get_holidays_per_period(period_id, employee_id), period_id
            ),
            period_id,
            employee_id,
        )
        for number in range(nbr_days_months):
            day = number + 1
            day_date = datetime(
                period_id.date_start.year, period_id.date_start.month, day
            )
            day_type = (
                special_days[day_date.strftime("%m%d%Y")]["day_type"]
                if day_date.strftime("%m%d%Y") in special_days
                else "1"
            )
            chantier_id = (
                special_days[day_date.strftime("%m%d%Y")]["chantier_id"]
                if day_date.strftime("%m%d%Y") in special_days
                and "chantier_id" in special_days[day_date.strftime("%m%d%Y")]
                else False
            )
            details = (
                special_days[day_date.strftime("%m%d%Y")]["details"]
                if day_date.strftime("%m%d%Y") in special_days
                else False
            )
            name = self._get_day(period_id, day)
            if "Dim" in name:
                day_type = "2"

            repport_lines.append(
                {
                    "name": name,
                    "day": day_date,
                    "day_type": str(day_type),
                    "rapport_id": rapport_id,
                    "employee_id": employee_id,
                    "details": details,
                    "chantier_id": chantier_id,
                }
            )

        return repport_lines

    def get_holidays_per_period(self, period_id, employee_id):
        holidays = self.env["hr.holidays"].search(
            [
                ("employee_id", "=", employee_id),
                ("state", "in", ("validate", "confirm")),
                "|",
                "|",
                "&",
                ("date_start", ">=", period_id.date_start),
                ("date_start", "<=", period_id.date_stop),
                "&",
                ("date_end", ">=", period_id.date_start),
                ("date_end", "<=", period_id.date_stop),
                "&",
                ("date_select_half_perso", ">=", period_id.date_start),
                ("date_select_half_perso", "<=", period_id.date_stop),
            ],
        )

        result = {}
        if holidays:
            for hold in holidays:
                remplacant = (
                    (" - Remplacer par : %s - %s")
                    % (
                        hold.remplacant_employee_id.cin,
                        hold.remplacant_employee_id.name,
                    )
                    if hold.remplacant_employee_id
                    else ""
                )
                motif_holiday = dict(
                    hold.fields_get(allfields=["motif"])["motif"]["selection"]
                )[hold.motif]
                if hold.demi_jour:
                    result[hold.date_select_half_perso.strftime("%m%d%Y")] = {
                        "day_type": "4",
                        "details": motif_holiday + remplacant,
                        "chantier_id": hold.chantier_id.id,
                        "emplacement_chantier_id": self.emplacement_chantier_id.id,
                    }
                else:
                    if (hold.date_start and hold.date_end) or (
                        hold.date_start and hold.demi_jour
                    ):
                        for single_date in self.env["account.month.period"].daterange(
                            hold.date_start,
                            hold.date_end if not hold.demi_jour else hold.date_start,
                        ):
                            result[single_date.strftime("%m%d%Y")] = {
                                "day_type": "4",
                                "details": motif_holiday + remplacant,
                                "chantier_id": hold.chantier_id.id,
                            }

        return result

    def get_jour_ferie_per_period(self, result, period_id):
        jour_feries = self.env["hr.jours.feries"].search(
            [
                ("state", "=", "validee"),
                "|",
                "&",
                ("date_start", ">=", period_id.date_start),
                ("date_start", "<=", period_id.date_stop),
                "&",
                ("date_end", ">=", period_id.date_start),
                ("date_end", "<=", period_id.date_stop),
            ],
        )
        if jour_feries:
            for jf in jour_feries:
                for single_date in self.env["account.month.period"].daterange(
                    jf.date_start, jf.date_end
                ):
                    result[single_date.strftime("%m%d%Y")] = {
                        "day_type": "3",
                        "details": jf.name,
                    }

        return result

    def get_declaration_per_period(self, result, period_id, employee_id):
        declaration = self.env["declaration.anomalie.employee.sur.chantier"].search(
            [
                ("employee_id", "=", employee_id),
                ("state", "in", ("valide", "approuved")),
                ("date_fait", ">=", period_id.date_start),
                ("date_fait", "<=", period_id.date_stop),
            ],
        )

        for dc in declaration:
            result[dc.date_fait.strftime("%m%d%Y")] = {
                "day_type": dc.type_declaration,
                "details": dc.motif,
                "chantier_id": dc.chantier_id.id,
            }

        return result
    
    def get_autorisation_deplacement_per_period(self, result, period_id, employee_id):
        deplacement_autorisation = self.env["hr.deplacement"].search(
            [
                ("employee_id", "=", employee_id),
                ("state", "in", ("valide", "approuved")),
                "|",
                "&",
                ("date_start", ">=", period_id.date_start),
                ("date_start", "<=", period_id.date_stop),
                "&",
                ("date_end", ">=", period_id.date_start),
                ("date_end", "<=", period_id.date_stop),
            ],
        )

        for dc in deplacement_autorisation:
            result[dc.date_fait.strftime("%m%d%Y")] = {
                "day_type": dc.type_declaration,
                "details": dc.motif,
            }

        return result

    def get_range_month(self, period_id):
        return calendar.monthrange(
            period_id.date_start.year, period_id.date_start.month
        )[1]

    def _get_day(self, period_id, day):
        locale.setlocale(locale.LC_TIME, self.env.context["lang"] + ".utf8")
        return (
            str("%02d" % day)
            + " "
            + datetime(period_id.date_start.year, period_id.date_start.month, day)
            .strftime("%a")
            .lower()
            .capitalize()
            .replace(".", "")
        )

    def get_first_n_characters(self, word, n):
        if word:
            if len(word) >= n:
                return word[:n]
        return word

    def is_pointeur(self):
        return self.env["res.users"].has_group("hr_management.group_pointeur")

    def create_update_payslip(self, redirect=True):
        view = self.env.ref("hr_management.fiche_paie_formulaire")

        nbr_jf_refunded = 0

        total_jour_travailler = 0
        if self.employee_id.contract_id.type_profile_related == 'j' and self.employee_id.contract_id.type_emp != 'o':
            total_jour_travailler = min(self.total_j_v + self.rapport_result()['j_transfert'],self.rapport_result()['jnt'])
        else:
            total_jour_travailler = self.total_j_v + self.rapport_result()['jdt'] + self.rapport_result()['j_transfert']

        data = {
            "employee_id": self.employee_id.id,
            "contract_id": self.employee_id.contract_id.id,
            "chantier_id": self.chantier_id.id,
            "period_id": self.period_id.id,
            "job_id": self.employee_id.job_id.id,
            "type_emp": self.employee_id.type_emp,
            "vehicle_id": self.vehicle_id.id,
            "emplacement_chantier_id": self.emplacement_chantier_id.id,
            "rapport_id": self.id,
            "quinzaine": self.quinzaine,
            "nbr_jour_travaille": total_jour_travailler,
            "nbr_heure_travaille": self.total_h_v,
            "autoriz_cp": self.employee_id.contract_id.completer_salaire_related,
            "autoriz_zero_cp": self.employee_id.contract_id.autoriz_zero_cp_related,
            "cotisation" : self.employee_id.cotisation,
            "amount_cimr" : self.employee_id.montant_cimr
        }

        if not self.payslip_ids:
            created_payroll = self.env["hr.payslip"].create(data)
            if redirect:
                return {
                    "name": ("Fiche de paie %s crée" % created_payroll.name),
                    "type": "ir.actions.act_window",
                    "view_type": "form",
                    "view_mode": "form",
                    "res_model": "hr.payslip",
                    "res_id": created_payroll.id,
                    "views": [(view.id, "form")],
                    "view_id": view.id,
                }
            else:
                return created_payroll
        else:
            if self.payslip_ids[0].payed_holidays:
                nbr_jf_refunded = self.count_nbr_ferier_days

            if self.payslip_ids[0].payed_worked_holidays:
                nbr_jf_refunded = self.count_nbr_ferier_days_v

            self.payslip_ids[0].write(
                {
                    "nbr_jour_travaille": min(self.total_j_v,self.rapport_result()['jnt']),
                    "nbr_heure_travaille": self.total_h_v,
                    "nbr_jf_refunded": nbr_jf_refunded,
                }
            )

    def action_validation(self):
        self.write({"state": "valide"})

    def action_draft(self):
        self.write({"state": "draft"})

    def action_cancel(self):
        self.write({"state": "cancel"})

    def action_done(self):
        self.write({"state": "done"})

    def action_working(self):
        if not self.employee_id.contract_id.pp_personnel_id_many2one:
            raise ValidationError(
                "Manque d'information, Cet employé n'a pas encors de profile de paie pour commancer le traitement. Veuillez régler la situation avant de procéder."
            )
        self.write({"state": "working"})
        for line in self.rapport_lines:
            line.j_travaille_v = self.employee_id.contract_id.get_hours_per_day(
                line.h_travailler_v
            )

    def get_half_month_day(self, period_id):
        period_month = period_id.date_start.month
        period_year = period_id.date_start.year
        return datetime.strptime(
            str(period_year) + "-" + str(period_month) + "-15", "%Y-%m-%d"
        ).date()

    def get_last_month_day(self):
        period_month = self.period_id.date_start.month
        period_year = self.period_id.date_start.year
        return datetime.strptime(
            str(period_year)
            + "-"
            + str(period_month)
            + "-"
            + str(calendar.monthrange(period_year, period_month)[1]),
            "%Y-%m-%d",
        ).date()

    def user_company_id(self):
        return self.chantier_id.cofabri

    @api.depends("employee_id")
    def _compute_type_employee(self):
        self.employee_type = self.employee_id.type_emp

    def group_worked_time(self):
        data = {}
        for line in self.rapport_lines:
            key = (
                line.chantier_id.id
                or 0 + line.emplacement_chantier_id.id
                or 0 + line.vehicle_id.id
                or 0
            )
            if key not in data:
                data[key] = {}
            data[key]["chantier_id"] = line.chantier_id.id
            data[key]["emplacement_chantier_id"] = line.emplacement_chantier_id.id
            data[key]["vehicle_id"] = line.vehicle_id.id
            if "h" in data[key]:
                data[key]["h"] += float(line.h_travailler_v)
            else:
                data[key]["h"] = float(line.h_travailler_v)

            if "j" in data[key]:
                data[key]["j"] += float(line.j_travaille_v)
            else:
                data[key]["j"] = float(line.j_travaille_v)

    def rapport_result(self):
        contract = self.employee_id.contract_id  # contrat par defaut
        type_emp = contract.type_emp
        type_profile = contract.type_profile_related
        jdt = self.count_nbr_dim_days_v # jour dimanche travaillé et validé par service rh
        jc = self.count_holiday_days_v  # jour congé validé par service rh
        jfnt = max(self.count_nbr_ferier_days - self.count_nbr_ferier_days_v ,0)# jour férie non travaillé 
        jf = self.count_nbr_ferier_days  # total des jour férié travaillé + non travaillé
        jom = self.jom  # jour ouvrable par mois
        joe = contract.nbre_jour_worked_par_mois_related if contract.definition_nbre_jour_worked_par_mois_related == "nbr_saisie" else self.period_id.get_number_of_days_per_month() # jour ouvrable sur lesquels le salaire de base de l'employé est définis
        default_day_2_add = joe - jom if contract.definition_nbre_jour_worked_par_mois_related == "nbr_saisie" else 0  # jour de réguralisation pour les mois exceptionnels (24-25-27)
        hnt = joe * contract.nbre_heure_worked_par_jour_related # heure de travail sur lesquelles le salaire de base de l'employé est définis
        jont = self.count_nbr_absense_days  # jour ouvrable non travaillé par le salarié
        ht = self.total_h_v  # heure travaillées par le salarié
        jt = self.total_j_v  # jour travaillées par le salarié
        h_comp = hnt - ht  # heure de compensation de salaire
        j_comp = joe - (jt + default_day_2_add) if type_profile == 'j' else h_comp / contract.nbre_heure_worked_par_jour_related # jour de compensation de salaire
        j_transfert = len(self.rapport_lines.filtered(lambda ln: ln.day_type == "9"))

        return {
            "jc": jc,
            "jdt": jdt,
            "jf": jf,
            "jfnt": jfnt,
            "jnt": joe,
            "jont": jont,
            "hnt": hnt,
            "ht": ht,
            "jt": jt,
            "j_transfert":j_transfert,
            "h_comp": h_comp,
            "j_comp": j_comp,
            "default_day_2_add": default_day_2_add,
        }

    def masse_payement(self):
        _ids = []
        for rec in self:
            res = rec.create_update_payslip(redirect=False)
            if res:
                _ids.append(res.id)
        tree_view = self.env.ref("hr_management.fiche_paie_tree")
        form_view = self.env.ref("hr_management.fiche_paie_formulaire")
        return {
            "name": ("Fiche de paie cadre pour mois %s" %self[0].name),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "hr.payslip",
            "views": [(tree_view.id, "tree"),(form_view.id, "form")],
            'domain':[('id','in',_ids)],
        }
