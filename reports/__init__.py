from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import cm 
import xlsxwriter
from connect import create_connection, close_connection
from psql_func.psql import list_of_expenses


def generate_pdf(user_id):
    '''This method generates an pdf file which contain all of the expenses and sum of the expenses'''
    pdf_filename = 'raport.pdf'

    cnx, cursor = create_connection()
    expenses = list_of_expenses(user_id, cursor)
    close_connection(cursor, cnx)

    texts = []
    sum_of_money = 0

    texts.append("RAPORT WYDATKÓW")

    for counter, expense in enumerate(expenses, 1):
        texts.append('''
        Wydatek {}
        Kategoria: {}
        Opis: {}
        Kwota: {} PLN
        '''.format(counter, expense[0], expense[2], expense[3]))
        sum_of_money += float(expense[3])

    texts.append("\n\n<h2>Lacznie: {} PLN</h2>".format(sum_of_money))    
    
    
    doc = SimpleDocTemplate(pdf_filename ,pagesize=A4,
                        rightMargin=2*cm,leftMargin=2*cm,
                        topMargin=2*cm,bottomMargin=2*cm)

    doc.build([Paragraph("\n\n".join(texts).replace("\n", "<br />"), getSampleStyleSheet()['Normal']),])



def generate_xls(user_id):
    '''This method generates XLS file with informations like category, description and price'''
    xls_filename = 'raport.xls'

    cnx, cursor = create_connection()
    expenses = list_of_expenses(user_id, cursor)
    close_connection(cursor, cnx)  

    workbook = xlsxwriter.Workbook(xls_filename)
    worksheet = workbook.add_worksheet()


    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})
    bold.set_align('center')

    # Add a number format for cells with money.
    money_format = workbook.add_format({'num_format': '#,##0 ZŁ'})
    money_format.set_align('center')

    # Adjust the column width.
    worksheet.set_column(1, 1, 20)
    worksheet.set_column(1, 2, 40)

    #center cells 
    cell_format = workbook.add_format()
    cell_format.set_align('center')


    worksheet.write('A1', 'Numer', bold)
    worksheet.write('B1', 'Kategoria', bold)
    worksheet.write('C1', 'Opis', bold)
    worksheet.write('D1', 'Koszt', bold)

    # Start from the first cell below the headers.
    row = 1
    col = 0
    money = 0
    counter = 1

    for expense in expenses:
     # Convert the date string into a datetime object.
        worksheet.write_number(row, col, counter, cell_format)
        worksheet.write_string(row, col + 1, expense[0], cell_format)
        worksheet.write_string(row, col + 2, expense[2], cell_format)
        worksheet.write_number(row, col + 3, expense[3], money_format)
        row += 1
        money += float(expense[3])
        counter += 1

    # Write a total using a formula.
    worksheet.write(row, 0, 'Łącznie', bold)
    worksheet.write(row, 3, '{}'.format(money), money_format)

    workbook.close()
