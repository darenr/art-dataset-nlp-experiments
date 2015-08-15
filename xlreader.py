import xlrd
import csv
import sys


def csv_from_excel(fname, sheet):
  wb = xlrd.open_workbook(fname)
  sh = wb.sheet_by_name(sheet)
  # your_csv_file = open('your_csv_file.csv', 'wb')
  #wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

  fieldnames = sh.row_values(0)

  for rownum in xrange(1, sh.nrows):
    #wr.writerow(sh.row_values(rownum))
    row = dict(zip(fieldnames, sh.row_values(rownum)))
    print row

    #your_csv_file.close()


if __name__ == "__main__":
  csv_from_excel(sys.argv[1], sys.argv[2])
