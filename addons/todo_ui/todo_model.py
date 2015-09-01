# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.addons.base.res import res_request
from openerp.exceptions import ValidationError


def referencable_models(self):
    return res_request.referencable_models(
        self, self.env.cr, self.env.uid, context=self.env.context)
    

class TodoTask(models.Model):
    _inherit = 'todo.task'
    _sql_constraints = [
        ('todo_task_name_uniq',
        'UNIQUE (name, user_id, active)',
        'Task title must be unique!')]
    stage_id = fields.Many2one('todo.task.stage', 'Stage')
    tag_ids = fields.Many2many('todo.task.tag', string='Tags')
    refers_to = fields.Reference(
        referencable_models, 'Refers to')
    stage_fold = fields.Boolean(
        string='Stage Folded?', 
        compute='_compute_stage_fold',
        # store=False) # the default
        search='_search_stage_fold',
        inverse='_write_stage_fold')
    stage_state = fields.Selection(
        related='stage_id.state',
        string='Stage State')
    user_todo_count = fields.Integer(
        'User To-Do Count',
        compute='compute_user_todo_count')
    
    @api.one
    @api.depends('stage_id.fold')
    def _compute_stage_fold(self):
        self.stage_fold = self.stage_id.fold
        
    def _search_stage_fold(self, operator, value):
        return [('stage_id.fold', operator, value)]
    
    def _write_stage_fold(self):
        self.stage_id.fold = self.stage_fold
    
    @api.one
    @api.constrains('name')
    def _check_name_size(self):
        if len(self.name) < 5:
            raise ValidationError('Must have 5 chars!')

    @api.one
    def compute_user_todo_count(self):
        self.user_todo_count = self.search_count(
            [('user_id', '=', self.user_id.id)])


class Tag(models.Model):
    _name = 'todo.task.tag'
    _parent_store = True
    # _parent_name = 'parent_id'
    name = fields.Char('Name', size=40, translate=True)
    parent_id = fields.Many2one(
        'todo.task.tag', 'Parent Tag', ondelete='restrict')
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)
    child_ids = fields.One2many(
        'todo.task.tag', 'parent_id', 'Child Tags')


class Stage(models.Model):
    _name = 'todo.task.stage'
    _order = 'sequence,name'
    # String fields:
    name = fields.Char('Name', size=40)
    desc = fields.Text('Description')
    state = fields.Selection(
    [('draft','New'), ('open','Started'),('done','Closed')],
    'State')
    docs = fields.Html('Documentation')
    # Numeric fields:
    sequence = fields.Integer('Sequence')
    perc_complete = fields.Float('% Complete', (3, 2))
    # Date fields:
    date_effective = fields.Date('Effective Date')
    date_changed = fields.Datetime('Last Changed')
    # Other fields:
    fold = fields.Boolean('Folded?')
    image = fields.Binary('Image')
    tasks = fields.One2many(
        'todo.task', # related model
        'stage_id', # field for "this" on related model
        'Tasks in this stage')

