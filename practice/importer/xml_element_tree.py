import xml.etree.ElementTree as ET
import csv


tree = ET.parse('icd10cm_tabular_2018.xml')
root = tree.getroot()
csv.register_dialect('custom_dialect', delimiter=';', quoting=csv.QUOTE_NONE)


def write_code(code):
    is_billable = False
    inner_codes = code.findall('diag')
    if inner_codes is not None:
        is_billable = True
    print(is_billable)


with open('chapters.csv', 'w') as chapters_file, open('sections.csv', 'w') as sections_file, \
        open('icd10.csv', 'w') as icd10_file:

    chapters_fieldnames = ['title', 'description']
    chapters_writer = csv.writer(chapters_file, dialect='custom_dialect')
    chapters_writer.writerow(chapters_fieldnames)

    sections_fieldnames = ['title', 'description', 'chapterTitle']
    sections_writer = csv.writer(sections_file, dialect='custom_dialect')
    sections_writer.writerow(chapters_fieldnames)

    for chapter in root.findall('chapter'):
        chapter_name = chapter.find('name').text.strip()
        chapter_description = chapter.find('desc').text.strip()
        chapters_writer.writerow([chapter_name, chapter_description])

        for section_ref in chapter.iter('sectionRef'):
            section_name = section_ref.get('id').strip()
            section_description = section_ref.text.strip()
            sections_writer.writerow([section_name, section_description, chapter_name])

        for section in chapter.findall('section'):
            section_name = section.get('id').strip()

            for code in section.findall('diag'):
                write_code(code)

