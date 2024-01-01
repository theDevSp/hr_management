# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import io
import xlrd
import babel
import logging
import tempfile
import binascii
from io import StringIO
from datetime import date, datetime, time
from odoo import api, fields, models, tools, _
from odoo.exceptions import Warning, UserError, ValidationError
_logger = logging.getLogger(__name__)

try:
	import csv
except ImportError:
	_logger.debug('Cannot `import csv`.')
try:
	import xlwt
except ImportError:
	_logger.debug('Cannot `import xlwt`.')
try:
	import cStringIO
except ImportError:
	_logger.debug('Cannot `import cStringIO`.')
try:
	import base64
except ImportError:
	_logger.debug('Cannot `import base64`.')


class ImportEmployee(models.TransientModel):
	_name = 'import.employee'
	_description = 'Import Employee'

	file_type = fields.Selection([('CSV', 'CSV File'),('XLS', 'XLS File')],string='File Type', default='CSV')
	file = fields.Binary(string="Upload File")

	def import_employee(self):
		if not self.file:
			raise ValidationError(_("Please Upload File to Import Employee !"))

		if self.file_type == 'CSV':
			line = keys = ['name','job_title','mobile_phone','work_phone','work_email','department_id','address_id','gender','birthday']
			try:
				csv_data = base64.b64decode(self.file)
				data_file = io.StringIO(csv_data.decode("utf-8"))
				data_file.seek(0)
				file_reader = []
				csv_reader = csv.reader(data_file, delimiter=',')
				file_reader.extend(csv_reader)
			except Exception:
				raise ValidationError(_("Please Select Valid File Format !"))
				
			values = {}
			for i in range(len(file_reader)):
				field = list(map(str, file_reader[i]))
				values = dict(zip(keys, field))
				if values:
					if i == 0:
						continue
					else:
						res = self.create_employee(values)
		else:
			try:
				file = tempfile.NamedTemporaryFile(delete= False,suffix=".xlsx")
				file.write(binascii.a2b_base64(self.file))
				file.seek(0)
				values = {}
				workbook = xlrd.open_workbook(file.name)
				sheet = workbook.sheet_by_index(0)
			except Exception:
				raise ValidationError(_("Please Select Valid File Format !"))

			for row_no in range(sheet.nrows):
				val = {}
				if row_no <= 0:
					fields = list(map(lambda row:row.value.encode('utf-8'), sheet.row(row_no)))
				else:
					line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
					print(xlrd.xldate_as_datetime(int(float(line[8])), 0).date().isoformat())
					values.update( {
							'name':line[0],
							'cin': line[1],
							'cnss': int(float(line[2])),
							'state_employee_wtf':line[3],
							'rib':line[4],
							'type_salaire':line[5],
							'type_employee':line[6],
							'type_contract':line[7],
							'date_start':xlrd.xldate_as_datetime(int(float(line[8])), 0).date().isoformat(),
							'wage':line[9],
							'profile':line[10],
							'chantier':line[11],
							'panier':line[12],
							'machine_id':line[13],
							'user_machine_id':line[14],
							})
					res = self.create_employee(values)


	def create_employee(self, values):
		employee = self.env['hr.employee']
		
		chantier_id = self.env['fleet.vehicle.chantier'].search([('code','=',values.get('chantier'))])[0]
		
		employee_vals = {
				'name' : values.get('name'),
				'cin' : values.get('cin'),
				'cnss' : values.get('cnss'),
				'state_employee_wtf' : values.get('state_employee_wtf'),
				'chantier_id':chantier_id.id,
				}

		employee_obj = employee.create(employee_vals)

		rib_vals = {
				'rib':values.get('rib'),
				}

		self.create_attach_rib(employee_obj=employee_obj,values=rib_vals)

		contract_vals = {
			'type_salaire':values.get('type_salaire'),
			'type_employee':values.get('type_employee'),
			'type_contract':values.get('type_contract'),
			'date_start':values.get('date_start'),
			'wage':values.get('wage'),
			'profile':values.get('profile'),
		}

		self.create_attach_contract(employee_obj=employee_obj,values=contract_vals)

		allocation_vals = {
			'name':'Régularisation aprés importation',
			'employee_id':employee_obj.id,
			'categorie':'regularisation',
			'nbr_jour':values.get('panier'),
			'period_id':self.env["account.month.period"].get_period_from_date(values.get('date_start'))[0].id 
		}
		self.create_attach_allocation(allocation_vals)

		return employee_obj
	
	def create_attach_rib(self,employee_obj,values):
		rib = self.env['employee.rib']
		rib_nunmber = rib.create({
			'name':(values.get('rib')),
			'payement_mode_id':1,
			'employee_id':employee_obj.id
		})
		if rib_nunmber:
			employee_obj.write({
				'rib_number':rib_nunmber.id
			})
		else:
			return
	
	def create_attach_contract(self,employee_obj,values):
		contract = self.env['hr.contract']

		type_salaire = [  
            ("h","Horaire"),
            ("j","Journalier"),
            ("m","MenSUel")
        ]
		type_salaire_key = list(filter(lambda sub, ele = values.get('type_salaire').lower() : ele in sub[1].lower(), type_salaire))

		type_employee = [
			("c","Cadre de Chantier"),
			("a","Administration"),
			("s","Salarié"),
			("o","Ouvrier")
			]
		type_employee_key = list(filter(lambda sub, ele = values.get('type_employee').lower() : ele in sub[1].lower(), type_employee))

		type_contract = self.env['hr.contract.type'].search([('name','=',values.get('type_contract'))])[0]

		profile_id = self.env['hr.profile.paie'].search([('code','=',values.get('profile'))])[0]

		contract_id = contract.create({
			'entreprise_id':1,
			'contract_type':type_contract.id,
			'type_salaire':type_salaire_key[0][0],
			'type_emp':type_employee_key[0][0],
			'wage':values.get('wage'),
			'employee_id':employee_obj.id,
			'date_start': values.get('date_start')
		})
		if contract_id:
			contract_id.to_running()
			contract_id.write({
				'profile_paie_id':profile_id.id
			})
			contract_id.generer_profile()
		else:
			return

	def create_attach_allocation(self,values):
		allocation = self.env['hr.allocations']
		allocation.create(values)
