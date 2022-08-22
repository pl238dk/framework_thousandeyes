import json
import requests
import urllib3
import base64
from time import sleep
urllib3.disable_warnings()

class thousand_eyes(object):
	def __init__(self, username, password):
		self.username = username
		self.password = password
		
		self.base_url = 'https://api.thousandeyes.com/v6/'
		
		un_pw = '{0}:{1}'.format(self.username, self.password)
		self.authorization_value = base64.b64encode(un_pw.encode('utf-8'))
		
		self.headers = {
			'format' : 'json',
			'Authorization' : 'Basic {0}'.format(self.authorization_value.decode('utf-8')),
		}
		
		self.proxy = {
			'https':''
		}
		return
	
	def initialize_aid(self):
		account_groups = self.account_group_list()
		for account in account_groups['accountGroups']:
			if account['accountGroupName'] == 'Your Company':
				self.aid = account['aid']
		return
	
	def get_list(self, list_type, querystring=None):
		_url = self.base_url + '{list_type}.json?aid={aid}{querystring}'.format(
			list_type = list_type,
			aid=self.aid if hasattr(self, 'aid') else '',
			querystring='&' + str(querystring) if querystring else '',
		)
		response = requests.get(
			_url,
			headers=self.headers,
			proxies=self.proxy,
			verify=False
		)
		if response.status_code == 200:
			response_json = json.loads(response.text)
			return response_json
		elif response.status_code == 429:
			while response.status_code != 200:
				print('[W] received 429, waiting to re-send "{}"'.format(list_type))
				sleep(5)
				response = requests.get(
					_url,
					headers=self.headers,
					proxies=self.proxy,
					verify=False
				)
			if response.status_code == 200:
				response_json = json.loads(response.text)
				return response_json
			else:
				print('[W] received {} for "{list_type}"'.format(response.status_code, list_type))
				return None
		else:
			print('[W] received {} for "{}"'.format(response.status_code, list_type))
			return None
	
	def post_list(self, list_type, data):
		_url = self.base_url + '{list_type}.json?aid={aid}'.format(
			list_type = list_type,
			aid=self.aid if hasattr(self, 'aid') else '',
		)
		
		self.headers['Content-Type'] = 'application/json'
		self.headers['Accept'] = 'application/json'
		
		response = requests.post(
			_url,
			headers=self.headers,
			proxies=self.proxy,
			data=json.dumps(data),
			verify=False
		)
		if response.status_code == 200:
			print(f'[I] POST successful!')
			response_json = json.loads(response.text)
			return response_json
		else:
			print(f'[W] POST unsuccessful! - {response.status_code} {response.text}')
			return None
	
	'''
	# no. too much metadata per instance
	def create_list(self, list_type):
		_url = self.base_url + '{list_type}.json?aid={aid}'.format(
			list_type = list_type,
			aid=self.aid if hasattr(self, 'aid') else '',
		)
		response = requests.post(
			_url,
			headers=self.headers,
			proxies=self.proxy,
			verify=False
		)
		if response.status_code == 200:
			response_json = json.loads(response.text)
			return response_json
		else:
			return None
	'''
	#
	#	BEGIN: GET
	#
	
	def status(self):
		response = self.get_list('status')
		return response
	
	def account_group_list(self, aid=None):
		_url = self.base_url + 'account-groups{aid}.json'.format(
			aid='/' + str(aid) if aid else ''
		)
		response = requests.get(
			_url,
			headers=self.headers,
			proxies=self.proxy,
			verify=False
		)
		if response.status_code == 200:
			response_json = json.loads(response.text)
	
		return response_json
		
	def test_list(self, testId=None):
		output = self.get_list('tests{testId}'.format(
			testId='/' + str(testId) if testId else ''
		))
		return output
	
	def test_list_by_type(self, test_type):
		types = [
			'agent-to-server',
			'agent-to-agent',
			'bgp',
			'http-server',
			'page-load',
			'transactions',
			'ftp-server',
			'dns-trace',
			'dns-server',
			'dns-dnssec',
			'dnsp-domain',
			'dnsp-server',
			'sip-server',
			'voice',
			'voice-call',
		]
		if test_type not in types:
			for type in types: print(type)
			return None
		output = self.get_list('tests/{test_type}'.format(
			test_type=test_type if test_type else ''
		))
		return output
	
	def agent_list(self, agentId=None):
		output = self.get_list('agents{agentId}'.format(
			agentId='/' + str(agentId) if agentId else ''
		))
		return output
	
	def agent_list_by_type(self, agent_type):
		types = [
			'CLOUD',
			'ENTERPRISE',
			'ENTERPRISE_CLUSTER',
		]
		if agent_type not in types:
			for type in types: print(type)
			return None
		output = self.get_list(
			'agents',
			querystring='agentTypes={agent_type}'.format(
				agent_type=agent_type
			),
		)
		return output
	
	def alert_rule_list(self, ruleId=None):
		output = self.get_list('alert-rules{ruleId}'.format(
			ruleId='/' + str(ruleId) if ruleId else ''
		))
		return output
	
	def alert_list(self, alertId=None):
		output = self.get_list('alerts{alertId}'.format(
			alertId='/' + str(alertId) if alertId else ''
		))
		return output
	
	def alert_integration_list(self):
		output = self.get_list('integrations')
		return output
	
	def alert_suppression_window_list(self, alertSupressionWindowId=None):
		output = self.get_list('alert-suppression-windows{alertSupressionWindowId}'.format(
			alertSupressionWindowId='/' + str(alertSupressionWindowId) if alertSupressionWindowId else ''
		))
		return output
	
	def label_list(self, groupId=None):
		output = self.get_list('groups{groupId}'.format(
			groupId='/' + str(groupId) if groupId else ''
		))
		return output
	
	def bgp_monitor_list(self):
		output = self.get_list('bgp-monitors')
		return output
	
	def report_list(self, reportId=None):
		output = self.get_list('reports{reportId}'.format(
			reportId='/' + str(reportId) if reportId else ''
		))
		return output
	
	def report_data_list(self, reportId, dataComponentId):
		output = self.get_list('reports/{reportId}/{dataComponentId}'.format(
			reportId,
			dataComponentId
		))
		return output
	
	def report_snapshot_list(self, snapshotId=None):
		output = self.get_list('report-snapshots{snapshotId}'.format(
			snapshotId='/' + str(snapshotId) if snapshotId else ''
		))
		return output
	
	def report_snapshot_data_list(self, snapshotId, dataComponentId):
		output = self.get_list('report-snapshots/{snapshotId}/{dataComponentId}'.format(
			snapshotId,
			dataComponentId
		))
		return output
	
	def user_list(self, uid=None):
		output = self.get_list('users{uid}'.format(
			uid='/' + str(uid) if uid else ''
		))
		return output
	
	def role_list(self, roleId=None):
		output = self.get_list('roles{roleId}'.format(
			roleId='/' + str(roleId) if roleId else ''
		))
		return output
	
	def permission_list(self):
		output = self.get_list('permissions')
		return output
	
	def usage_list(self):
		output = self.get_list('usage')
		return output
	
	def endpoint_user_session_list(self, sessionId=None):
		output = self.get_list('endpoint-data/user-sessions{sessionId}'.format(
			sessionId='/' + str(sessionId) if sessionId else ''
		))
		return output
	
	def endpoint_web_pages_list(self, sessionId=None, pageId=None):
		if not sessionId and not pageId:
			output = self.get_list('endpoint-data/user-sessions/web')
		else:
			output = self.get_list('endpoint-data/user-sessions/{sessionId}/page/{pageId}'.format(
				sessionId,
				pageId
			))
		return output
	
	def endpoint_network_session_list(self):
		output = self.get_list('endpoint-data/user-sessions/network')
		return output
	
	def endpoint_network_topology_list(self, networkProbeId=None):
		output = self.get_list('endpoint-data/network-topology{networkProbeId}'.format(
			networkProbeId='/' + str(networkProbeId) if networkProbeId else ''
		))
		return output
	
	def endpoint_agent_list(self, agentId=None):
		output = self.get_list('endpoint-agents{agentId}'.format(
			agentId='/' + str(agentId) if agentId else ''
		))
		return output
	
	def endpoint_network_list(self):
		output = self.get_list('endpoint-data/networks')
		return output
	
	def get_test_by_name(self, test_name):
		if len(test_name) == 15 and test_name[-2:].isdigit():
			# skip if uppercase
			correct_test_name = '{bu}{device}{pole}{location}'.format(
				bu=test_name[:3].upper(),
				device=test_name[3:5].lower(),
				pole=test_name[5:8].upper(),
				location=test_name[8:].lower(),
			)
		else:
			print('failed to find test : incorrect name format\ntest_name: {}'.format(test_name))
			return None
		all_tests = self.test_list()
		output = [x for x in all_tests['test'] if x['testName'] == correct_test_name]
		return output
	
	def get_test_by_server(self, server):
		all_tests = self.test_list()
		output = [x for x in all_tests['test'] if 'server' in x and x['server'] == server]
		return output
	#
	#	END: GET
	#
	#	BEGIN: POST
	#
	def test_create(self, test_name, server):
		if len(test_name) == 15 and test_name[-2:].isdigit():
			# skip if uppercase
			correct_test_name = '{bu}{device}{pole}{location}'.format(
				bu=test_name[:3].upper(),
				device=test_name[3:5].lower(),
				pole=test_name[5:8].upper(),
				location=test_name[8:].lower(),
			)
		else:
			print('failed to create test : incorrect name format\ntest_name: {} - server: {}'.format(test_name, server))
			return None
		server_ip_only = server if '/' not in server else server.split('/')[0]
		data = {
			'testName':correct_test_name,
			'interval':300,
			'server': server_ip_only,
			'protocol':'ICMP',
			'port':'',
		#	'agents':[{'agentId':x} for x in pole],
			'agents':[],
		#	'alertsEnabled':1,
			'alertsEnabled':0,
		#	'groups':[{'groupId':pole_label}],
			'groups':[],
		}
		
		flag_names = {
		}
		
		print(data)
		output = self.post_list('tests/agent-to-server/new', data)
		return output
	
	def test_standardize(self, test):
		if len(test['testName']) == 15 and test['testName'][-2:].isdigit():
			# skip if uppercase
			correct_test_name = '{bu}{device}{pole}{location}'.format(
				bu=test['testName'][:3].upper(),
				device=test['testName'][3:5].lower(),
				pole=test['testName'][5:8].upper(),
				location=test['testName'][8:].lower(),
			)
		else:
			print('failed to create test : incorrect name format\ntest_name: {} - server: {}'.format(test['testName'], test['server']))
			return None
		data = {
			'testName':correct_test_name,
			'interval':300,
			'server': test['server'],
			'protocol':'ICMP',
			'port':'',
		#	'agents':[{'agentId':x} for x in pole],
			'agents':[],
		#	'alertsEnabled':1,
			'alertsEnabled':0,
		#	'groups':[{'groupId':pole_label}],
			'groups':[],
		}
		
		output = self.post_list('tests/agent-to-server/{test_id}/update'.format(test_id=test['testId']), data)
		return output
	
	def test_delete(self, test_id):
		output = self.post_list('tests/agent-to-server/{test_id}/delete'.format(test_id=test_id),None)
		return output
	
	def test_enable_alerts(self, test_id):
		data = {
			'alertsEnabled':1,
		}
		output = self.post_list('tests/agent-to-server/{test_id}/update'.format(test_id=test_id), data)
		return output
	
	def test_disable_alerts(self, test_id):
		data = {
			'alertsEnabled':0,
		}
		output = self.post_list('tests/agent-to-server/{test_id}/update'.format(test_id=test_id), data)
		return output
	
	def test_update_field(self, test_id, _field, _value):
		data = {
			_field: _value,
		}
		output = self.post_list('tests/agent-to-server/{test_id}/update'.format(test_id=test_id), data)
		return output
	#
	#	END: POST
	#
	
if __name__ == '__main__':
	te_api_username = ''
	te_api_password = ''
	te = thousand_eyes(te_api_username, te_api_password)
    te.initialize_aid()
