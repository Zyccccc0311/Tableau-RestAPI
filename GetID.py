"""You need to install tableauserverclient before you run this script"""


import tableauserverclient as TSC

#Your server URL
Onlineservername='http://win-nc0gjlgvtt5/'
tableau_auth = TSC.TableauAuth('admin', 'admin', '')
server = TSC.Server(Onlineservername)

with server.auth.sign_in(tableau_auth):

  all_workbooks_items, pagination_item = server.workbooks.get()
  print([workbook.id for workbook in all_workbooks_items])

  print([workbook.name for workbook in all_workbooks_items])