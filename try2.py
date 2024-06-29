import xlsxwriter

# Create a workbook and add a worksheet
workbook = xlsxwriter.Workbook('example.xlsx')
worksheet = workbook.add_worksheet()

# Create a format with the desired font properties
font_format = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'bold': True})

# Apply the format to a cell
worksheet.write('A1', 'Hello, World!', font_format)

# Close the workbook
workbook.close()
