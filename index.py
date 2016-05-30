import run

parser = run.Parser("http://164.100.129.6/netnrega/st_weightage_drill.aspx?lflag=eng&fin_year=2016-2017")
run.statusLog = 'status.csv'
run.doc_load_time = 10

run.routes = []
strings = "parser.rule1,//*[@id='ctl00_ContentPlaceHolder1_gvEmployee']/tbody/tr/td[2]/a,State :,0,5;parser.rule2,//*[@id='ctl00_ContentPlaceHolder1_gvEmployee'];parser.rule1,//*[@id='ctl00_ContentPlaceHolder1_gvEmployee']/tbody/tr/td[2]/a,District :,1,3;parser.rule2,//*[@id='ctl00_ContentPlaceHolder1_gvEmployee'];parser.rule1,//*[@id='ctl00_ContentPlaceHolder1_gvEmployee']/tbody/tr/td[2]/a,Block  : ,2,1;parser.rule2,//*[@id='ctl00_ContentPlaceHolder1_gvEmployee']".split(';')
for string in strings:
	string = string.split(',')
	obj = run.Route()
	method_name = string.pop(0)
	methods = {'parser.rule1': parser.rule1,'parser.rule2': parser.rule2}
	if method_name in methods:
		obj.method_name = methods[method_name]
	obj.arguments = string
	run.routes.append(obj)

#run.DOWNLOAD_PATH = "/home/rohit/swachBharat/I2/Downloads/"
parser.configBrowser()
parser.getData()
