import pandas as pd
import numpy as np
from xlsxwriter.utility import xl_rowcol_to_cell

df = pd.read_excel("sampledata.xlsx")

startrowval = 2 # index starts from zero
writer = pd.ExcelWriter('sample_enhanced_output.xlsx', engine='xlsxwriter')
df.to_excel(writer, startrow=startrowval, index=False, sheet_name='report')


workbook = writer.book
worksheet = writer.sheets['report']
#Now we have the worksheet object. We can manipulate it 
worksheet.set_zoom(90)

#Set header formating
header_format = workbook.add_format({
        "valign": "vcenter",
        "align": "center",
        "bg_color": "#951F06",
        "bold": True,
        'font_color': '#FFFFFF'
    })


#add title
title = "Monthly Sales Report "
#merge cells
format = workbook.add_format()
format.set_font_size(20)
format.set_font_color("#333333")
#
subheader = "Sales report for Classic Vest, M"
worksheet.merge_range('A1:AS1', title, format)
worksheet.merge_range('A2:AS2', subheader)
worksheet.set_row(2, 15) # Set the header row height to 15
# puting it all together
# Write the column headers with the defined format.
for col_num, value in enumerate(df.columns.values):
    #print(col_num, value)
    worksheet.write(startrowval, col_num, value, header_format)



# Add a number format for cells with money.
money_fmt = workbook.add_format({'num_format': '$#,##0.00'})
# Total formatting
total_fmt = workbook.add_format({'align': 'right', 'num_format': '$#,##0',
                                 'bold': True, 'bottom':6})

# Adjust the column width.
worksheet.set_column('A:F', 20)


# numeric columns
worksheet.set_column('F:I', 12, money_fmt)


number_rows = len(df.index) + startrowval



# Add total rows
for column in range(5, 9):
    # Determine where we will place the formula
    cell_location = xl_rowcol_to_cell(number_rows+1, column)
    # Get the range to use for the sum formula
    start_range = xl_rowcol_to_cell(3, column)
    print(start_range)
    end_range = xl_rowcol_to_cell(number_rows, column)
    print(end_range)
    # Construct and write the formula
    formula = "=SUM({:s}:{:s})".format(start_range, end_range)
    print(formula)
    worksheet.write_formula(cell_location, formula, total_fmt)

    
# Add a total label
worksheet.write_string(number_rows+1, 4, "Total",total_fmt)

#Advance output
# writer.save()
writer.close()