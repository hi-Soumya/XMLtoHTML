import xml.etree.ElementTree as Eltr 
import webbrowser
import os 
import tkinter as tktr 
from tkinter import Text, messagebox

def Convert_to_html(input_xml_string):
    try:
        root = Eltr.fromstring(input_xml_string)
        html_table = "<table border='2'>\n"

        # Extract field names and field types 
        field_names = []
        field_types = []
        first_row = root.find('row')
        if first_row is not None:
            for field in first_row.findall('field'):
                field_names.append(field.attrib.get('name', ''))
                field_types.append(field.attrib.get('type', ''))

        # Create table headers <th>
        html_table += " <tr>\n"
        for field_name in field_names:
            html_table += f"  <th>{field_name}</th>\n"
        html_table += " </tr>\n"

        # Process each row
        for row in root.findall('row'):
            html_table += "  <tr>\n"
            for field_name, field_type in zip(field_names, field_types):
                field = row.find(f"field[@name='{field_name}']")
                if field is not None:
                    field_value = field.attrib.get('value', '')
                    if field_type != 'collection':
                        html_table += f"  <td> {field_value} </td>\n"
                    elif field_type == 'collection':
                        # Decode the nested collection in the XML string and process it
                        nested_collection_xml = Eltr.fromstring(field_value)
                        nested_html = Convert_to_html(Eltr.tostring(nested_collection_xml, encoding='unicode'))
                        html_table += f"  <td> {nested_html} </td>\n"
                else:
                    html_table += " <td></td>\n"
            html_table += "  </tr>\n"
        html_table += "</table>"

        return html_table
    except Exception as excep:
        messagebox.showerror("Error", f"An error occurred: {excep}")
        return None

def create_html():
    input_xml_string = xml_text.get('1.0', 'end-1c')
    html_table = Convert_to_html(input_xml_string)

    if html_table:
        fileName_html = 'output.html'
        with open(fileName_html, 'w') as f:
            f.write(html_table)

        webbrowser.open('file://' + os.path.realpath(fileName_html))

root = tktr.Tk()
root.title("BluePrism XML to HTML Converter")

xml_text = tktr.Text(root, width=100, height=30, wrap=tktr.WORD)
xml_text.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

generate_button = tktr.Button(root, text="Generate HTML", command=create_html)
generate_button.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

root.columnconfigure(0, weight=5)
root.rowconfigure(0, weight=5)

root.mainloop()
