# -*- coding: utf-8 -*-
######################################################################################
#
#    Captivea
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################

{
    'name': 'Budget Analysis Enhancement',
    'version': '15.0.0.1',
    'summary': 'Enhanced data for analyzing budgets',
    'description': """This module gives additional insight into budgets based on PO sate.              
                """,
    'category': 'Accounting',
    'author': 'Bassim Elsamaloty',
    'company': 'Captivea LLC',
    'maintainer': 'https://www.captivea.com/',    
    'depends': ['base', 'account', 'purchase', 'analytic', 'account_budget'],
    'website': 'https://www.captivea.com/',
    'data': [
        'views/crossovered_budget.xml',
        'views/purchase_order_view.xml',
    ],
    'qweb': [],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
