from bs4 import BeautifulSoup
import requests

class Scraper:
    def __init__(self, curr_url, data):
        """Here we get html source code and current URL"""
        page = requests.get(curr_url)
        doc = BeautifulSoup(page.content, "html.parser")
        rows = doc.find_all("tr")
        self.rows = rows[3:-1:1]
        self.data = data
        self.current_date = None

        self.rowspan_dict = {"Date": [],
                             "Number": [],
                             "Hour": [],
                             "Discipline": [],
                             "Room": [],
                             "Teacher": []}

        for row in self.rows:
            columns = row.find_all("td")
            self.analyzing_row(columns)

    def analyzing_row(self, columns):
        if columns[0].attrs.get("id") is not None:
            self.analyzing_day_of_week(columns)

        elif columns[0].string == "Няма занятия":
            self.analyzing_rest_day()

        else:
            self.analyzing_working_days(columns)

    def analyzing_working_days(self, columns):
        if len(columns) > 1 and columns[1].attrs.get("rowspan") is not None:
            rowspan_num = int(columns[1].attrs.get("rowspan"))
            for idx in range(0, 5):
                columns[idx] = columns[idx].string
                ''' Ако columns[idx] е NoneTypeObject хвърля грешка при метода replace() '''
                try:
                    columns[idx] = columns[idx].replace('\n', '')
                    columns[idx] = columns[idx].replace('\t', '')
                except:
                    columns[idx] = ''
            self.data["Date"].append(self.current_date)
            self.data["Number"].append(columns[0])
            self.data["Hour"].append(columns[1])
            self.data["Discipline"].append(columns[2])
            self.data["Room"].append(columns[3])
            self.data["Teacher"].append(columns[4])

            self.add_rowdata_to_rowspan_dict(rowspan_num)  # duplicate last data to rowspan dict
        elif self.checking_rowspan_dictionary_is_not_clear():
            self.add_rowspandict_data_to_datadict()
        else:
            if len(columns) == 5:
                for idx in range(0, 5):
                    columns[idx] = columns[idx].string
                    ''' Ако columns[idx] е NoneTypeObject хвърля грешка при метода replace() '''
                    try:
                        columns[idx] = columns[idx].replace('\n', '')
                        columns[idx] = columns[idx].replace('\t', '')
                    except:
                        columns[idx] = ''
                self.data["Date"].append(self.current_date)
                self.data["Number"].append(columns[0])
                self.data["Hour"].append(columns[1])
                self.data["Discipline"].append(columns[2])
                self.data["Room"].append(columns[3])
                self.data["Teacher"].append(columns[4])

            else:  # Defect rows
                self.data["Date"].append(self.current_date)
                self.data["Number"].append(columns[0].string)
                self.data["Hour"].append('')
                self.data["Discipline"].append('')
                self.data["Room"].append('')
                self.data["Teacher"].append('')

    def analyzing_rest_day(self):
        self.data["Date"].append(self.current_date)
        self.data["Number"].append("Няма занятия")
        self.data["Hour"].append("")
        self.data["Discipline"].append("")
        self.data["Room"].append("")
        self.data["Teacher"].append("")

    def analyzing_day_of_week(self, columns):
        date = columns[0].string
        self.current_date = date

    def checking_rowspan_dictionary_is_not_clear(self):
        return len(self.rowspan_dict['Date']) > 0

    def add_rowspandict_data_to_datadict(self):
        self.data["Date"].append(self.rowspan_dict["Date"].pop(0))
        self.data["Number"].append(self.rowspan_dict["Number"].pop(0))
        self.data["Hour"].append(self.rowspan_dict["Hour"].pop(0))
        self.data["Discipline"].append(self.rowspan_dict["Discipline"].pop(0))
        self.data["Room"].append(self.rowspan_dict["Room"].pop(0))
        self.data["Teacher"].append(self.rowspan_dict["Teacher"].pop(0))

    def add_rowdata_to_rowspan_dict(self, rowspan_num):
        rowspan_num = rowspan_num - 1
        number = int(self.data["Number"][-1])
        counter = 1
        while rowspan_num > 0:
            self.rowspan_dict["Date"].append(self.data["Date"][-1])
            self.rowspan_dict["Number"].append(str(number + counter))
            self.rowspan_dict["Hour"].append(self.data["Hour"][-1])
            self.rowspan_dict["Discipline"].append(self.data["Discipline"][-1])
            self.rowspan_dict["Room"].append(self.data["Room"][-1])
            self.rowspan_dict["Teacher"].append(self.data["Teacher"][-1])
            rowspan_num -= 1
            counter += 1
